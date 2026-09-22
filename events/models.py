from django.db import models
from accounts.models import VendorProfile


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)


class Event(models.Model):
    STATUS_CHOICES = [("draft", "Draft"), ("published", "Published"), ("cancelled", "Cancelled")]

    vendor = models.ForeignKey(VendorProfile, on_delete=models.PROTECT, related_name="events")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    venue = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    total_seats = models.PositiveIntegerField()
    available_seats = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="draft")

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(available_seats__gte=0), name="seats_non_negative"),
        ]

    def save(self, *args, **kwargs):
        if self._state.adding and not self.available_seats:
            self.available_seats = self.total_seats
        super().save(*args, **kwargs)