from django.http import HttpResponseRedirect
from django.conf import settings
from allauth.account.views import ConfirmEmailView

class CustomConfirmEmailView(ConfirmEmailView):

    def get(self, request, *args, **kwargs):
        try:
            self.object = self.get_object()
            self.object.confirm(request)
            # Redirect on success
            return HttpResponseRedirect(f"{settings.WEBSITE_FRONTEND_URL}/email-verified")
        except Exception as e:
            # Log the error for debugging
            print(f"Error confirming email: {e}")
            # Fallback: render the template
            return self.render_to_response(self.get_context_data())
