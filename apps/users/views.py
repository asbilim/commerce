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

User = get_user_model()

class GoogleLoginView(SocialLoginView):
    adapter_class = GoogleOAuth2Adapter
    callback_url = f"{settings.WEBSITE_FRONTEND_URL}/auth/google/callback/"  # Update this
    client_class = OAuth2Client

    def get_response(self):
        response = super().get_response()
        
        if self.user and not self.user.is_verified:
            self.user.is_verified = True
            self.user.save()
            
        return response

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