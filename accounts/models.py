import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    CUSTOMER = "customer"
    VENDOR = "vendor"
    STAFF = "staff"

    ROLE_CHOICES = [(CUSTOMER, "Customer"),(VENDOR, "Vendor"), (STAFF, "Staff")]
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=20,choices=ROLE_CHOICES,default=CUSTOMER)
    referral_code = models.CharField( max_length=20, unique=True, blank=True)
    referred_by = models.ForeignKey("self", on_delete=models.SET_NULL, null=True,blank=True,related_name="referrals")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):

        if not self.referral_code:
            self.referral_code = uuid.uuid4().hex[:10].upper()

        super().save(*args, **kwargs)
class VendorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="vendor_profile")
    company_name = models.CharField(max_length=255)
    gst_number = models.CharField(max_length=30, blank=True)
    address = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)