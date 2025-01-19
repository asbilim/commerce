from dj_rest_auth.registration.views import RegisterView
from allauth.account.utils import send_email_confirmation
from rest_framework.exceptions import APIException
from rest_framework import status

from django.utils.translation import gettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from apps.users.api.serializers import CustomPasswordResetConfirmSerializer
from dj_rest_auth import app_settings


class CustomPasswordResetConfirmView(GenericAPIView):
    """
    Confirms the password reset e-mail link and resets the user's password.

    Accepts the following POST parameters: token, uid,
        new_password1, new_password2
    Returns the success/fail message.
    """
    serializer_class = CustomPasswordResetConfirmSerializer
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

class CustomRegisterView(RegisterView):
    def perform_create(self, serializer):
        user = serializer.save(self.get_cleaned_data())
        try:
            # Attempt to send email confirmation
            send_email_confirmation(self.request, user)
        except Exception as e:
            # If email sending fails, delete the user and raise an error
            user.delete()
            raise APIException(
                detail="Email confirmation could not be sent. Please try again.",
                code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
        return user
