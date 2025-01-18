from django.contrib import admin
from django.urls import path, include, re_path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from apps.users.views import CustomConfirmEmailView

urlpatterns = [
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('admin/', admin.site.urls),
    path('auth/', include('dj_rest_auth.urls')),
    re_path(
        r'^auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$',
        CustomConfirmEmailView.as_view(),
        name='account_confirm_email',
    ),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path(r'^accounts/', include('allauth.urls')),
    
]