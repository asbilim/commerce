# users/views.py

from django.utils.translation import gettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from dj_rest_auth import app_settings


class CustomPasswordResetConfirmView(GenericAPIView):
    """
    Confirms the password reset e-mail link and resets the user's password.

    Accepts the following POST parameters: token, uid,
        new_password1, new_password2
    Returns the success/fail message.
    """
    serializer_class = app_settings.DEFAULTS['PASSWORD_RESET_CONFIRM_SERIALIZER']
    permission_classes = (AllowAny,)
    throttle_scope = 'dj_rest_auth'

    @method_decorator(sensitive_post_parameters('new_password1', 'new_password2'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Handle POST request to reset the user's password.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'detail': _('Password has been reset with the new password.')},
            status=status.HTTP_200_OK,
        )
