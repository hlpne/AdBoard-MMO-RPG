"""
Admin configuration for newsletters app.
"""
from django.contrib import admin
from .models import Subscription, NewsletterTemplate, NewsletterSendJob


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    """Subscription admin."""
    list_display = ['user', 'is_active', 'created_at', 'updated_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['user__email']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['user']


@admin.register(NewsletterTemplate)
class NewsletterTemplateAdmin(admin.ModelAdmin):
    """NewsletterTemplate admin."""
    list_display = ['title', 'created_at']
    search_fields = ['title']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'


@admin.register(NewsletterSendJob)
class NewsletterSendJobAdmin(admin.ModelAdmin):
    """NewsletterSendJob admin."""
    list_display = ['template', 'status', 'total', 'sent', 'errors', 'started_at', 'finished_at']
    list_filter = ['status', 'started_at']
    search_fields = ['template__title']
    readonly_fields = ['started_at', 'finished_at']
    raw_id_fields = ['template']
    date_hierarchy = 'started_at'

