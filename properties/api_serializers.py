"""
API Serializers

WHAT THIS FILE DOES:
- Converts Python objects to JSON (and vice versa)
- Validates API data
- Defines what fields to include in API responses

TOPICS TO LEARN:
- Django REST Framework
- Serializers
- JSON conversion
- API data structure
"""

from rest_framework import serializers
from locations.models import Location
from properties.models import Property
from images.models import PropertyImage


# LOCATION SERIALIZER

class LocationSerializer(serializers.ModelSerializer):
    """
    Serializer for Location model
    
    WHAT THIS DOES:
    Converts Location objects to JSON
    """
    
    class Meta:
        model = Location
        fields = ['id', 'name', 'city', 'state', 'country']


# PROPERTY IMAGE SERIALIZER

class PropertyImageSerializer(serializers.ModelSerializer):

    # Serializer for PropertyImage model

    class Meta:
        model = PropertyImage
        fields = ['id', 'image', 'caption', 'is_primary']


# PROPERTY LIST SERIALIZER

class PropertyListSerializer(serializers.ModelSerializer):
    """
    Serializer for Property list view (summary info)
    
    WHAT THIS DOES:
    - Shows basic property info for list view
    - Includes nested location data
    - Includes first image URL
    """
    
    # Nested serializer for location
    location = LocationSerializer(read_only=True)
    
    # Custom field using a model method
    first_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Property
        fields = [
            'id', 'title', 'location', 'property_type',
            'bedrooms', 'bathrooms', 'max_guests',
            'price_per_night', 'first_image', 'is_available'
        ]
    
    def get_first_image(self, obj):
        """
        Get the first image URL
        
        WHAT THIS DOES:
        - obj = Property object
        - Calls model method get_first_image()
        - Returns image URL or None
        """
        return obj.get_first_image()


# PROPERTY DETAIL SERIALIZER

class PropertyDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Property detail view (full info)
    
    WHAT THIS DOES:
    - Shows all property information
    - Includes all images (not just first)
    - Includes amenities as list
    """
    
    # Nested location
    location = LocationSerializer(read_only=True)
    
    # Multiple images (many=True)
    images = PropertyImageSerializer(many=True, read_only=True)
    
    # Amenities as list
    amenities_list = serializers.SerializerMethodField()
    
    class Meta:
        model = Property
        fields = [
            'id', 'title', 'description', 'location',
            'property_type', 'bedrooms', 'bathrooms', 'max_guests',
            'price_per_night', 'address', 'amenities', 'amenities_list',
            'images', 'is_available', 'created_at', 'updated_at'
        ]
    
    def get_amenities_list(self, obj):
        """Get amenities as a list"""
        return obj.get_amenities_list()