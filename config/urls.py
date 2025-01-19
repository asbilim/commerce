from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from allauth.socialaccount.providers.google.views import oauth2_login
from apps.users.views import CustomConfirmEmailView, GoogleLoginView, GoogleOneTapView
from django.views.generic import TemplateView
from apps.users.api.serializers import CustomPasswordResetConfirmView

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(
        r'^auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$',
        CustomConfirmEmailView.as_view(),
        name='account_confirm_email',
    ),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path(r'^accounts/', include('allauth.urls')),
    path('auth/callback/', include('allauth.socialaccount.providers.google.urls')),
    path('auth/google/onetap/', GoogleOneTapView.as_view(), name='google_onetap'),
    path('auth/google/', GoogleLoginView.as_view(), name='google_login'),
    path('auth/password/reset/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('auth/', include('dj_rest_auth.urls')),
    path('test/google/',TemplateView.as_view(template_name="backend/auth/test/google.html")),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    
]


if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path(r'^__debug__/', include(debug_toolbar.urls)),
    ]