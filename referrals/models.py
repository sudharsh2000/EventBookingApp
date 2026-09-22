from django.conf import settings
from django.db import models

POSITION_CHOICES = [("left", "Left"), ("right", "Right")]


class ReferralNode(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="referral_node")
    sponsor = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="direct_referrals")
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL, related_name="children")
    position = models.CharField(max_length=5, choices=POSITION_CHOICES, null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["parent", "position"], condition=models.Q(parent__isnull=False), name="one_child_per_position")
        ]

    @property
    def left_child(self):
        return self.children.filter(position="left").first()

    @property
    def right_child(self):
        return self.children.filter(position="right").first()