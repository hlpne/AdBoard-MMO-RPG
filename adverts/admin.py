"""
Admin configuration for adverts app.
"""
from django.contrib import admin
from .models import Category, Advert, MediaAsset


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category admin."""
    list_display = ['slug', 'name']
    search_fields = ['slug', 'name']
    readonly_fields = ['slug']


@admin.register(Advert)
class AdvertAdmin(admin.ModelAdmin):
    """Advert admin."""
    list_display = ['title', 'author', 'category', 'status', 'created_at']
    list_filter = ['status', 'category', 'created_at']
    search_fields = ['title', 'body_md', 'author__email']
    readonly_fields = ['created_at', 'updated_at', 'body_html']
    date_hierarchy = 'created_at'
    raw_id_fields = ['author', 'category']
    
    actions = ['make_published', 'make_archived']
    
    def make_published(self, request, queryset):
        queryset.update(status=Advert.Status.PUBLISHED)
    make_published.short_description = 'Опубликовать выбранные'
    
    def make_archived(self, request, queryset):
        queryset.update(status=Advert.Status.ARCHIVED)
    make_archived.short_description = 'Архивировать выбранные'


@admin.register(MediaAsset)
class MediaAssetAdmin(admin.ModelAdmin):
    """MediaAsset admin."""
    list_display = ['file', 'type', 'owner', 'mime', 'size', 'created_at']
    list_filter = ['type', 'mime', 'created_at']
    search_fields = ['owner__email', 'file']
    readonly_fields = ['created_at', 'mime', 'size', 'width', 'height', 'duration']
    date_hierarchy = 'created_at'
    raw_id_fields = ['owner']

