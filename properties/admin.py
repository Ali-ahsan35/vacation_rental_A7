"""
Property Admin Configuration

WHAT THIS FILE DOES:
- Customizes how Property model appears in Django Admin
- Allows uploading MULTIPLE images directly on property edit page (INLINE)
- Adds filters and search
"""

from django.contrib import admin
from .models import Property
from images.models import PropertyImage  # Import PropertyImage for inline


# INLINE IMAGE UPLOAD 

class PropertyImageInline(admin.TabularInline):

    model = PropertyImage  # The model to display inline
    extra = 3  
    fields = ['image', 'caption', 'is_primary']


# PROPERTY ADMIN 

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    """
    Admin interface for Property model
    """
    
    # COLUMNS TO DISPLAY in the list view
    list_display = [
        'title',           # Property name
        'location',        # Which location (shows __str__ of Location)
        'property_type',   # Villa, Cabin, etc.
        'bedrooms',        # Number of bedrooms
        'bathrooms',       # Number of bathrooms
        'price_per_night', # Price
        'is_available',    # Available? (green checkmark or red X)
        'created_at'       # When created
    ]
    
    # FILTERS on the right sidebar
    list_filter = [
        'is_available',      # Filter by available/not available
        'property_type',     # Filter by type (Villa, Cabin, etc.)
        'location__city',    # Filter by location city (notice the __)
        'location__state',   # Filter by location state
        'bedrooms',          # Filter by number of bedrooms
        'created_at'         # Filter by date created
    ]
    # location__city is called "field lookup"
    # It accesses the city field of the related Location model
    
    # SEARCH BAR
    search_fields = [
        'title',            # Search by property title
        'description',      # Search in description
        'location__name',   # Search by location name
        'location__city',   # Search by location city
        'address'           # Search by address
    ]
    
    # DEFAULT ORDERING
    ordering = ['-created_at']  # Newest first (- means descending)
    
    # READ-ONLY FIELDS
    readonly_fields = ['created_at', 'updated_at']
    
    # INLINE MODELS (upload images on the same page!)
    inlines = [PropertyImageInline]
    # This adds the image upload section to the property edit page
    
    # FORM ORGANIZATION
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'location')
        }),
        ('Property Details', {
            'fields': ('property_type', 'bedrooms', 'bathrooms', 'max_guests')
        }),
        ('Pricing', {
            'fields': ('price_per_night',)
        }),
        ('Address', {
            'fields': ('address',)
        }),
        ('Amenities', {
            'fields': ('amenities',),
            'description': 'Enter amenities separated by commas (e.g., WiFi,Pool,Kitchen)'
        }),
        ('Availability', {
            'fields': ('is_available',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        """
        Optimize database queries
        
        WHAT THIS DOES:
        When loading the property list, also load related location data
        This prevents multiple database queries (N+1 problem)
        """
        queryset = super().get_queryset(request)
        return queryset.select_related('location')
        # select_related() loads related Location in one query
        # Instead of 100 queries for 100 properties, only 1 query total


