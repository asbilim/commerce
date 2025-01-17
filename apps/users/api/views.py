from dj_rest_auth.registration.views import RegisterView
from allauth.account.utils import send_email_confirmation
from rest_framework.exceptions import APIException
from rest_framework import status

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
