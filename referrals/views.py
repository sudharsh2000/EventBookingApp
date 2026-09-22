from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from referrals.models import ReferralNode
from referrals import services


class ReferralTreeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        node = get_object_or_404(ReferralNode, user_id=user_id)
        depth = int(request.query_params.get("depth", 5))
        return Response(services.build_tree(node, depth))


class ReferralRootAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        node = get_object_or_404(ReferralNode, user_id=user_id)
        root = services.get_root(node)
        return Response({"root_user_id": root.user_id, "root_email": root.user.email})


class ReferralStatsAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        node = get_object_or_404(ReferralNode, user_id=user_id)
        return Response(services.get_team_stats(node))