# apps/users/views.py

from django.http import HttpResponseRedirect
from django.conf import settings
from allauth.account.views import ConfirmEmailView
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView
from django.contrib.auth import get_user_model
from config.settings.auth import AuthenticationConfig
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.response import Response

User = get_user_model()

class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = settings.WEBSITE_FRONTEND_URL  # Update this to match your frontend URL
    client_class = OAuth2Client

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            if response.status_code == 200:
                # Customize the response data if needed
                response.data['message'] = 'Successfully authenticated with Google'
            return response
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class CustomConfirmEmailView(ConfirmEmailView):
    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            confirmation = self.object.confirm(request)
            
            auth_config = AuthenticationConfig.get_settings()
            frontend_url = auth_config['FRONTEND']['BASE_URL']
            success_path = auth_config['FRONTEND']['SUCCESS_REDIRECT']

            redirect_url = f"{frontend_url}{success_path}"

            context = {
                'redirect_url': redirect_url,
                'user': confirmation.email_address.user
            }
            
            response = render_to_string(
                auth_config['EMAIL']['VERIFICATION_TEMPLATE'],
                context,
                request
            )
            
            return HttpResponseRedirect(redirect_url)
            
        except Exception as e:
            print(f"Error confirming email: {e}")
            error_path = auth_config['FRONTEND']['ERROR_REDIRECT']
            return HttpResponseRedirect(f"{frontend_url}{error_path}")
        

class GoogleOneTapView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    client_class = OAuth2Client
    callback_url = "http://localhost:8000/"  # Not strictly used in One Tap, but required by allauth

    def post(self, request, *args, **kwargs):
        """
        We override post() to move 'id_token' into 'access_token',
        because allauth/dj-rest-auth expect an 'access_token' by default.
        """
        # Safely extract id_token from request.data
        id_token = request.data.get('id_token', None)
        if not id_token:
            return Response(
                {'error': 'No id_token provided'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Hack: rename it to 'access_token'
        mutable_data = request.data.copy()
        mutable_data['access_token'] = id_token
        request._full_data = mutable_data

        # Now let the parent handle it
        return super().post(request, *args, **kwargs)