"""
Admin configuration for replies app.
"""
from django.contrib import admin
from .models import Reply


@admin.register(Reply)
class ReplyAdmin(admin.ModelAdmin):
    """Reply admin."""
    list_display = ['advert', 'author', 'status', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at', 'updated_at']
    search_fields = ['text', 'advert__title', 'author__email']
    readonly_fields = ['created_at', 'updated_at']
    raw_id_fields = ['advert', 'author']
    date_hierarchy = 'created_at'

