"""Binary tree placement + traversal. Called from accounts on registration."""
from collections import deque
from django.db import transaction
from accounts.models import User
from referrals.models import ReferralNode
from core.exceptions import InvalidReferralCode


def resolve_sponsor(referral_code):
    if not referral_code:
        return None
    sponsor = User.objects.filter(referral_code=referral_code.strip().upper()).first()
    if sponsor is None:
        raise InvalidReferralCode(f"No user with referral code '{referral_code}'.")
    return sponsor


@transaction.atomic
def place_in_binary_tree(user, sponsor):
    node = ReferralNode.objects.create(user=user)
    if sponsor is None:
        return node

    sponsor_node = ReferralNode.objects.select_for_update().get(user=sponsor)
    queue = deque([sponsor_node])
    parent = position = None

    while queue and parent is None:
        current = queue.popleft()
        children = {c.position: c for c in current.children.select_for_update().all()}
        for pos in ("left", "right"):
            if pos not in children:
                parent, position = current, pos
                break
        else:
            queue.append(children["left"])
            queue.append(children["right"])

    node.sponsor = sponsor
    node.parent = parent
    node.position = position
    node.save()
    return node


def get_root(node):
    while node.parent_id:
        node = node.parent
    return node


def _descendants_by_parent(root):
    mapping = {}
    frontier = [root.pk]
    while frontier:
        children = list(ReferralNode.objects.filter(parent_id__in=frontier).select_related("user"))
        if not children:
            break
        for c in children:
            mapping.setdefault(c.parent_id, []).append(c)
        frontier = [c.pk for c in children]
    return mapping


def get_team_stats(node):
    mapping = _descendants_by_parent(node)

    def subtree_size(n):
        return sum(len(v) for v in _descendants_by_parent(n).values()) if n else 0

    left, right = node.left_child, node.right_child
    left_count = (1 + subtree_size(left)) if left else 0
    right_count = (1 + subtree_size(right)) if right else 0
    return {
        "user_id": node.user_id, "referral_code": node.user.referral_code,
        "left_team_count": left_count, "right_team_count": right_count,
        "total_team_count": left_count + right_count,
    }


def build_tree(node, max_depth=5):
    mapping = _descendants_by_parent(node)

    def to_dict(n, depth):
        children = {c.position: c for c in mapping.get(n.pk, [])}
        out = {"id": n.user_id, "email": n.user.email, "referral_code": n.user.referral_code,
               "position": n.position, "left": None, "right": None}
        if depth < max_depth:
            for side in ("left", "right"):
                child = children.get(side)
                out[side] = to_dict(child, depth + 1) if child else None
        return out

    return to_dict(node, 0)