from django.conf import settings
from django.db import models
from events.models import Event


class Booking(models.Model):
    STATUS_CHOICES = [("confirmed", "Confirmed"), ("cancelled", "Cancelled")]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="bookings")
    event = models.ForeignKey(Event, on_delete=models.PROTECT, related_name="bookings")
    quantity = models.PositiveIntegerField()
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="confirmed")
    created_at = models.DateTimeField(auto_now_add=True)