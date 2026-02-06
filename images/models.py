"""
PropertyImage Model

WHAT THIS FILE DOES:
- Defines the PropertyImage table in the database
- CONNECTS to Property model (ForeignKey relationship)
- Each property can have multiple images

DATABASE TABLE: images_propertyimage
RELATIONSHIP: PropertyImage (many) -> Property (one)
"""

from django.db import models
from properties.models import Property  # ← IMPORT Property from properties app!


class PropertyImage(models.Model):
    """
    Represents an image for a property
    One property can have many images
    """
    
    # FOREIGN KEY - Link to Property table
    property = models.ForeignKey(
        Property,
        on_delete=models.CASCADE,
        related_name='images' 
    )
    #This creates a "Many-to-One" relationship
    # Many images can belong to one property
    
    
    # Image FILE FIELD - Image file upload
    image = models.ImageField(
        upload_to='property_images/',
        help_text="Upload property image"
    )
    #Stores image files in media/property_images/ folder
    
    
    # VARCHAR(200) - Image caption (optional)
    caption = models.CharField(
        max_length=200, 
        blank=True, 
        null=True,
        help_text="Optional image caption"
    )
    
    
    # BOOLEAN - Is this the primary/cover image?
    is_primary = models.BooleanField(
        default=False, 
        help_text="Set as primary/cover image"
    )
    
    
    # DATETIME - When was this uploaded?
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        ordering = ['-is_primary', 'uploaded_at']  # Primary images first, then by upload date
        verbose_name = 'Property Image'
        verbose_name_plural = 'Property Images'
    
    
    def __str__(self):
        """String representation"""
        return f"Image for {self.property.title}"
    
    
    def save(self, *args, **kwargs):
        """
        Override save method to ensure only one primary image per property
        
        WHAT THIS DOES:
        If this image is marked as primary, remove primary flag from other images
        """
        if self.is_primary:
            # Find all other images for this property that are marked as primary
            PropertyImage.objects.filter(
                property=self.property,                     # Same property
                is_primary=True                             # Currently marked as primary
            ).exclude(pk=self.pk).update(is_primary=False)  # Except this one, set to False
        
        # Call the parent save method
        super().save(*args, **kwargs)
