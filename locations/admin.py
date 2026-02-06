"""
Location Admin Configuration

WHAT THIS FILE DOES:
- Customizes how Location model appears in Django Admin
- Adds filters, search, and display options
- Makes it easy to manage locations
"""

from django.contrib import admin
from .models import Location


@admin.register(Location)
# this decorator registers the Location model with this admin class
class LocationAdmin(admin.ModelAdmin):
    """
    Admin interface for Location model
    """
    
    # COLUMNS TO DISPLAY in the list view
    list_display = ['name', 'city', 'state', 'country', 'created_at']

    # FILTERS on the right sidebar. we can filter by country, state, or city
    list_filter = ['country', 'state', 'city']

    search_fields = ['name', 'city', 'state', 'country']
    
    # Locations are sorted alphabetically by name (A-Z)
    ordering = ['name']
     
    # READ-ONLY FIELDS (can't edit these)
    readonly_fields = ['created_at', 'updated_at']
    
    # FORM ORGANIZATION (groups fields together)
    fieldsets = (
        ('Location Information', {
            'fields': ('name', 'city', 'state', 'country')
        }),
        ('Description', {
            'fields': ('description',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)  # This section is collapsed by default
        }),
    )

