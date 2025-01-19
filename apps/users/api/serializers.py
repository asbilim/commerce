# apps/users/api/serializers.py

from dj_rest_auth.serializers import PasswordResetConfirmSerializer
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

class CustomPasswordResetConfirmSerializer(PasswordResetConfirmSerializer):
    new_password1 = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'},
        label=_("New Password"),
    )
    new_password2 = serializers.CharField(
        required=True,
        write_only=True,
        style={'input_type': 'password'},
        label=_("Confirm New Password"),
    )

    def validate(self, attrs):
        # You can add custom validation logic here if needed
        return super().validate(attrs)

    def save(self, **kwargs):
        return super().save(**kwargs)
