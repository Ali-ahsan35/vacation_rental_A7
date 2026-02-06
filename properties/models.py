"""
Property Model

WHAT THIS FILE DOES:
- Defines the Property table in the database
- CONNECTS to Location model (ForeignKey relationship)
- Each property belongs to one location

DATABASE TABLE: properties_property
RELATIONSHIP: Property (many) -> Location (one)
"""

from django.db import models
from locations.models import Location  # ← IMPORT Location from locations app!


class Property(models.Model):
    """
    Represents a vacation rental property
    """
    
    # ==================== BASIC INFORMATION ====================
    
    # VARCHAR(300) - Property title
    title = models.CharField(
        max_length=300,
        help_text="Property title/name"
    )
    
    # TEXT - Property description
    description = models.TextField(
        help_text="Detailed description of the property"
    )
    
    # FOREIGN KEY - Link to Location table
    location = models.ForeignKey(
        Location,  # ← The model we're linking to
        on_delete=models.SET_NULL,  # If location is deleted, set this to NULL
        related_name='properties',  # Access all properties from a location: location.properties.all()
        null=True,  # Can be NULL (empty)
        blank=True,  # Can be empty in forms
        help_text="Assign location after importing"
    )
    # Many properties can belong to one location
    
    
    # ==================== PROPERTY DETAILS ====================
    
    # VARCHAR(100) - Type of property
    property_type = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        help_text="Type: Villa, Cabin, House, Condo, etc."
    )
    
    # INTEGER - Number of bedrooms
    bedrooms = models.IntegerField(
        default=1,
        help_text="Number of bedrooms"
    )
    
    # DECIMAL - Number of bathrooms (can be 2.5, 3.5, etc.)
    bathrooms = models.DecimalField(
        max_digits=3,  # Total digits: 3
        decimal_places=1,  # Decimal places: 1 (e.g., 2.5)
        default=1.0,
        help_text="Number of bathrooms"
    )
    
    # INTEGER - Maximum guests allowed
    max_guests = models.IntegerField(
        default=2,
        help_text="Maximum number of guests"
    )
    
    
    # ==================== PRICING ====================
    
    # DECIMAL - Price per night
    price_per_night = models.DecimalField(
        max_digits=10,  # Up to 10 digits total
        decimal_places=2,  # 2 decimal places (e.g., 450.00)
        help_text="Nightly rental price"
    )
    
    
    # ==================== ADDRESS ====================
    
    # VARCHAR(500) - Full address
    address = models.CharField(
        max_length=500, 
        blank=True, 
        null=True,
        help_text="Full street address"
    )
    
    
    # ==================== AMENITIES ====================
    
    # TEXT - Comma-separated amenities
    amenities = models.TextField(
        blank=True, 
        null=True, 
        help_text="Comma-separated amenities (e.g., WiFi,Pool,Kitchen)"
    )
    
    
    # ==================== AVAILABILITY ====================
    
    # BOOLEAN - Is property available for booking?
    is_available = models.BooleanField(
        default=True,
        help_text="Is this property available?"
    )
    
    
    # ==================== TIMESTAMPS ====================
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    class Meta:
        ordering = ['-created_at']  # Newest first
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
    
    
    def __str__(self):
        """String representation"""
        return self.title
    
    
    def get_first_image(self):
        """
        Get the first image for this property
        Returns the image URL or None
        """
        first_image = self.images.first()  # Access related images
        return first_image.image.url if first_image else None
    
    
    def get_amenities_list(self):
        """
        Convert comma-separated amenities to a list
        Example: "WiFi,Pool,Kitchen" -> ["WiFi", "Pool", "Kitchen"]
        """
        if self.amenities:
            return [amenity.strip() for amenity in self.amenities.split(',')]
        return []

