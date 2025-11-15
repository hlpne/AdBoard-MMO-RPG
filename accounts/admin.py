"""
Admin configuration for accounts app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, EmailVerification, UserProfile


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin."""
    list_display = ['email', 'username', 'is_active', 'is_staff', 'date_joined']
    list_filter = ['is_active', 'is_staff', 'is_superuser', 'date_joined']
    search_fields = ['email', 'username']
    ordering = ['-date_joined']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'first_name', 'last_name')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )


@admin.register(EmailVerification)
class EmailVerificationAdmin(admin.ModelAdmin):
    """EmailVerification admin."""
    list_display = ['user', 'code', 'is_used', 'created_at', 'expires_at']
    list_filter = ['is_used', 'created_at', 'expires_at']
    search_fields = ['user__email', 'code']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """UserProfile admin."""
    list_display = ['user', 'nickname', 'created_at']
    search_fields = ['user__email', 'nickname']
    readonly_fields = ['created_at', 'updated_at']

