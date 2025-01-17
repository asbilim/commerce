# apps/users/models.py
from core.models import UUIDModel
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django_countries.fields import CountryField
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType

from django.core.validators import RegexValidator
from django_countries.fields import CountryField


PHONE_TYPES = [
    ('MOBILE', 'Mobile'),
    ('HOME', 'Home'),
    ('WORK', 'Work'),
]

class User(UUIDModel, AbstractUser):
    """
    Custom user with UUID primary key and distinct related_name for groups & perms
    """
    # Override M2M to avoid name collisions with 'auth.User'
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',  # was 'user_set' by default
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',  # was 'user_set' by default
        blank=True
    )
    email = models.EmailField(_('email address'), unique=True)
    date_of_birth = models.DateField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    email_marketing = models.BooleanField(default=True)
    sms_marketing = models.BooleanField(default=True)
    two_factor_enabled = models.BooleanField(default=False)
    tos_accepted = models.BooleanField(default=False)
    tos_accepted_at = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.tos_accepted and not self.tos_accepted_at:
            self.tos_accepted_at = timezone.now()
        super().save(*args, **kwargs)



class Address(models.Model):
    """
    Address model that can also have phone numbers associated with it.
    """
    ADDRESS_TYPES = [
        ('SHIPPING', 'Shipping'),
        ('BILLING', 'Billing'),
        ('BOTH', 'Both'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    address_type = models.CharField(max_length=8, choices=ADDRESS_TYPES, default='SHIPPING')
    is_primary = models.BooleanField(default=False)

    full_name = models.CharField(max_length=255)
    street_address1 = models.CharField(max_length=255)
    street_address2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state_province = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = CountryField()

    # If you want phone numbers attached to addresses generically:
    phones = GenericRelation('Phone', related_query_name='address_owner')

    def __str__(self):
        return f"{self.full_name} ({self.address_type})"

    class Meta:
        verbose_name_plural = 'Addresses'
        ordering = ['-is_primary']


class Phone(models.Model):
    """
    A generic phone model that can link to any object needing a phone number:
    - user.phones
    - address.phones
    - etc.
    """
    phone_type = models.CharField(
        max_length=10,
        choices=PHONE_TYPES,
        default='MOBILE'
    )
    # Store country code separately, e.g. "+1", "+44"
    country_code = models.CharField(max_length=5, blank=True)

    # If you need more robust validation, consider django-phonenumber-field
    phone_regex = RegexValidator(
        regex=r'^[0-9]{6,15}$',
        message=_("Phone number must contain only digits (6-15 digits).")
    )
    number = models.CharField(
        validators=[phone_regex],
        max_length=15
    )

    is_verified = models.BooleanField(default=False)
    is_primary = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Generic foreign key fields
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.get_phone_type_display()}: {self.country_code}{self.number}"

    class Meta:
        verbose_name = "Phone Number"
        verbose_name_plural = "Phone Numbers"