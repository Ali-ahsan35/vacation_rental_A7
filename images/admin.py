"""
PropertyImage Admin Configuration

WHAT THIS FILE DOES:
- Customizes how PropertyImage appears in Django Admin
- Shows image thumbnails in the list view
- Shows larger preview in the edit form
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import PropertyImage


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    """
    Admin interface for PropertyImage model
    """
    
    # COLUMNS TO DISPLAY (including custom thumbnail column!)
    list_display = ['image_thumbnail', 'property', 'caption', 'is_primary', 'uploaded_at']
    # EXPLANATION: 'image_thumbnail' is a custom method we'll define below
    
    # FILTERS
    list_filter = ['is_primary', 'uploaded_at', 'property__location']
    # EXPLANATION: Can filter by:
    # - Is primary image?
    # - Upload date
    # - Property location
    
    # SEARCH BAR
    search_fields = ['property__title', 'caption']
    # EXPLANATION: Search by property title or image caption
    
    # DEFAULT ORDERING
    ordering = ['-uploaded_at']  # Newest uploads first
    
    # READ-ONLY FIELDS (including custom preview!)
    readonly_fields = ['image_preview', 'uploaded_at']
    # EXPLANATION: 'image_preview' is a custom method we'll define below
    
    # FORM ORGANIZATION
    fieldsets = (
        ('Image Information', {
            'fields': ('property', 'image', 'image_preview')
        }),
        ('Details', {
            'fields': ('caption', 'is_primary')
        }),
        ('Metadata', {
            'fields': ('uploaded_at',),
            'classes': ('collapse',)
        }),
    )
    
    
    # ==================== CUSTOM METHODS ====================
    
    def image_thumbnail(self, obj):
        """
        Display small thumbnail in list view
        
        WHAT THIS DOES:
        Shows a small preview of the image in the admin list
        Instead of just seeing filename, you see the actual image!
        """
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 100px; height: 60px; object-fit: cover;" />',
                obj.image.url
            )
        return "No Image"
    
    image_thumbnail.short_description = 'Thumbnail'
    # EXPLANATION: This sets the column header name
    
    
    def image_preview(self, obj):
        """
        Display larger preview in detail view
        
        WHAT THIS DOES:
        Shows a larger preview when editing an image
        Helpful to see what image you're working with
        """
        if obj.image:
            return format_html(
                '<img src="{}" style="max-width: 500px; max-height: 400px;" />',
                obj.image.url
            )
        return "No Image"
    
    image_preview.short_description = 'Image Preview'

