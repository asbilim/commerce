# apps/users/admin.py

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _

from unfold.admin import ModelAdmin as UnfoldModelAdmin

from import_export.admin import ImportExportModelAdmin
from import_export import resources

from .models import User, Address, Phone


# 1. Define Import-Export Resources
class UserResource(resources.ModelResource):
    class Meta:
        model = User
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name',
            'date_of_birth', 'is_active', 'is_verified',
            'email_marketing', 'sms_marketing', 'two_factor_enabled',
            'tos_accepted', 'tos_accepted_at', 'date_joined'
        )
        export_order = fields


class AddressResource(resources.ModelResource):
    class Meta:
        model = Address
        fields = (
            'id', 'user', 'address_type', 'is_primary',
            'full_name', 'street_address1', 'street_address2',
            'city', 'state_province', 'postal_code', 'country', 'phone_number'
        )
        export_order = fields


class PhoneResource(resources.ModelResource):
    class Meta:
        model = Phone
        fields = (
            'id', 'phone_type', 'country_code', 'number',
            'is_verified', 'is_primary', 'created_at', 'updated_at',
            'content_type', 'object_id'
        )
        export_order = fields


# 2. Define Custom User Forms
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = (
            'email', 'username', 'first_name', 'last_name',
            'date_of_birth', 'avatar', 'is_active',
            'is_verified', 'email_marketing', 'sms_marketing',
            'two_factor_enabled', 'tos_accepted', 'tos_accepted_at',
            'groups', 'user_permissions'
        )


# 3. Register Custom User Admin
@admin.register(User)
class CustomUserAdmin(ImportExportModelAdmin, DjangoUserAdmin):
    """
    Custom User Admin integrating:
    - django-import-export for data import/export
    - Inherits from Django's built-in UserAdmin
    """
    resource_class = UserResource
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = User

    list_display = ('email', 'username', 'is_active', 'is_verified', 'date_joined')
    list_filter = ('is_active', 'is_verified', 'is_staff', 'date_joined')
    search_fields = ('email', 'username', 'first_name', 'last_name')
    ordering = ('-date_joined',)

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('username', 'first_name', 'last_name', 'date_of_birth', 'avatar')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Verification'), {'fields': ('is_verified', 'two_factor_enabled')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Marketing'), {'fields': ('email_marketing', 'sms_marketing')}),
        (_('TOS'), {'fields': ('tos_accepted', 'tos_accepted_at')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2')
        }),
    )


# 4. Register Address Admin
@admin.register(Address)
class AddressAdmin(ImportExportModelAdmin, UnfoldModelAdmin):
    """
    Address Admin integrating:
    - django-import-export for data import/export
    - django-unfold for enhanced UI
    """
    resource_class = AddressResource
    list_display = ('id', 'user', 'address_type', 'full_name', 'city', 'country', 'is_primary')
    list_filter = ('address_type', 'is_primary', 'country')
    search_fields = ('full_name', 'city', 'postal_code', 'user__email')
    ordering = ('-is_primary', 'full_name')
    readonly_fields = ('id',)


# 5. Register Phone Admin
@admin.register(Phone)
class PhoneAdmin(ImportExportModelAdmin, UnfoldModelAdmin):
    """
    Phone Admin integrating:
    - django-import-export for data import/export
    - django-unfold for enhanced UI
    """
    resource_class = PhoneResource
    list_display = ('id', 'phone_type', 'country_code', 'number', 'is_verified', 'is_primary', 'created_at')
    list_filter = ('phone_type', 'is_verified', 'is_primary')
    search_fields = ('number', 'user__email')  # Adjust if using GenericForeignKey
    ordering = ('-is_primary', 'phone_type')
    readonly_fields = ('id', 'created_at', 'updated_at')
