import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.utils import timezone


# Create your models here.

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email=None, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    username = None
    email = models.EmailField(_("email address"), unique=True, blank=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return f"{str(self.email)}"


class VendorDetail(models.Model):
    vendor_code = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name = models.CharField(max_length=150, null=True, blank=True)
    contact_details = models.CharField(max_length=20, null=True, blank=True, help_text="Phone number!")
    address = models.CharField(max_length=350, null=True, blank=True)
    on_time_delivery_rate = models.FloatField(null=True, blank=True, default=0)
    quality_rating_avg = models.FloatField(null=True, blank=True, default=0)
    average_response_time = models.FloatField(null=True, blank=True, default=0)
    fulfillment_rate = models.FloatField(null=True, blank=True, default=0)

    def __str__(self):
        return self.full_name


STATUS_CHOICES = (("PENDING", "pending"),
                  ("COMPLETED", "completed"),
                  ("CANCELED", "canceled"))


class PurchaseOrder(models.Model):
    po_number = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    vendor = models.ForeignKey(VendorDetail, on_delete=models.CASCADE, null=True, blank=True)
    order_date = models.DateTimeField(null=True, blank=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    items = models.JSONField(null=True, blank=True)
    quantity = models.IntegerField(null=True, blank=True)
    status = models.CharField(max_length=120, choices=STATUS_CHOICES, null=True, blank=True)
    quality_rating = models.FloatField(blank=True, null=True)
    issue_date = models.DateTimeField(null=True, blank=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.vendor}/{self.po_number}"


class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(VendorDetail, on_delete=models.CASCADE, blank=True, null=True)
    date = models.DateTimeField(null=True, blank=True)
    on_time_delivery_rate = models.FloatField(blank=True, null=True)
    quality_rating_avg = models.FloatField(blank=True, null=True)
    average_response_time = models.FloatField(blank=True, null=True)
    fulfillment_rate = models.FloatField(blank=True, null=True)




