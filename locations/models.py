"""
Location Model

WHAT THIS FILE DOES:
- Defines the Location table in the database
- Each location can have multiple properties

DATABASE TABLE: locations_location
COLUMNS: id, name, city, state, country, description, created_at, updated_at
"""

from django.db import models


class Location(models.Model):
    """
    Represents a location where properties are located
    Example: Miami Beach, Florida, USA
    """
    
    # VARCHAR(200) - Location name (unique, no duplicates)
    name = models.CharField(
        max_length=200, 
        # unique=True,
        help_text="Location name (e.g., Miami Beach)"
    )
    
    # VARCHAR(100) - City name
    city = models.CharField(
        max_length=100,
        help_text="City name"
    )
    
    # VARCHAR(100) - State/Province name
    state = models.CharField(
        max_length=100,
        help_text="State or province"
    )
    
    # VARCHAR(100) - Country name (default: USA)
    country = models.CharField(
        max_length=100, 
        default='USA',
        help_text="Country name"
    )
    
    # TEXT - Optional description
    description = models.TextField(
        blank=True, 
        null=True,
        help_text="Optional description of the location"
    )
    
    # DATETIME - Automatically set when created
    created_at = models.DateTimeField(auto_now_add=True)
    
    # DATETIME - Automatically updated when modified
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        """
        Meta options for the model
        """
        ordering = ['name']  # Default ordering by name A-Z
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
        constraints = [
            models.UniqueConstraint(
                fields=["name", "city", "country"],
                name="unique_location"
            )
        ]
    
    def __str__(self):
        """
        String representation of the object
        This is what shows in Django admin dropdowns
        """
        return f"{self.name}, {self.state}, {self.country}"
        # Example output: "Miami Beach, Florida, USA"