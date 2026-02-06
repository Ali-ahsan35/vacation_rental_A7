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


# ==================== LOCATION SERIALIZER ====================

class LocationSerializer(serializers.ModelSerializer):
    """
    Serializer for Location model
    
    WHAT THIS DOES:
    Converts Location objects to JSON
    
    Example output:
    {
        "id": 1,
        "name": "Miami Beach",
        "city": "Miami",
        "state": "Florida",
        "country": "USA"
    }
    """
    
    class Meta:
        model = Location
        fields = ['id', 'name', 'city', 'state', 'country']
        # EXPLANATION:
        # - model = Which model to serialize
        # - fields = Which fields to include in JSON


# ==================== PROPERTY IMAGE SERIALIZER ====================

class PropertyImageSerializer(serializers.ModelSerializer):
    """
    Serializer for PropertyImage model
    
    Example output:
    {
        "id": 1,
        "image": "/media/property_images/villa.jpg",
        "caption": "Beautiful exterior",
        "is_primary": true
    }
    """
    
    class Meta:
        model = PropertyImage
        fields = ['id', 'image', 'caption', 'is_primary']


# ==================== PROPERTY LIST SERIALIZER ====================

class PropertyListSerializer(serializers.ModelSerializer):
    """
    Serializer for Property list view (summary info)
    
    WHAT THIS DOES:
    - Shows basic property info for list view
    - Includes nested location data
    - Includes first image URL
    
    Example output:
    {
        "id": 1,
        "title": "Luxury Villa",
        "location": {
            "id": 1,
            "name": "Miami Beach",
            "city": "Miami",
            "state": "Florida",
            "country": "USA"
        },
        "property_type": "Villa",
        "bedrooms": 5,
        "bathrooms": "4.5",
        "max_guests": 10,
        "price_per_night": "450.00",
        "first_image": "/media/property_images/villa.jpg",
        "is_available": true
    }
    """
    
    # Nested serializer for location
    location = LocationSerializer(read_only=True)
    # EXPLANATION:
    # - LocationSerializer = Use Location serializer
    # - read_only=True = Can't create location through this API
    # - This includes full location data in the response
    
    # Custom field using a model method
    first_image = serializers.SerializerMethodField()
    # EXPLANATION:
    # - SerializerMethodField = Custom calculated field
    # - Calls get_first_image() method below
    
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


# ==================== PROPERTY DETAIL SERIALIZER ====================

class PropertyDetailSerializer(serializers.ModelSerializer):
    """
    Serializer for Property detail view (full info)
    
    WHAT THIS DOES:
    - Shows all property information
    - Includes all images (not just first)
    - Includes amenities as list
    
    Example output:
    {
        "id": 1,
        "title": "Luxury Villa",
        "description": "Beautiful beachfront property...",
        "location": {...},
        "property_type": "Villa",
        "bedrooms": 5,
        "bathrooms": "4.5",
        "max_guests": 10,
        "price_per_night": "450.00",
        "address": "123 Ocean Drive",
        "amenities": "WiFi,Pool,Kitchen",
        "amenities_list": ["WiFi", "Pool", "Kitchen"],
        "images": [
            {"id": 1, "image": "/media/...", ...},
            {"id": 2, "image": "/media/...", ...}
        ],
        "is_available": true,
        "created_at": "2024-01-15T10:30:00Z",
        "updated_at": "2024-01-15T10:30:00Z"
    }
    """
    
    # Nested location
    location = LocationSerializer(read_only=True)
    
    # Multiple images (many=True)
    images = PropertyImageSerializer(many=True, read_only=True)
    # EXPLANATION:
    # - many=True = Multiple images
    # - read_only=True = Can't create images through this API
    
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


"""
SERIALIZERS EXPLAINED:

Serializers convert between Python objects and JSON

class MySerializer(serializers.ModelSerializer):
    class Meta:
        model = MyModel
        fields = ['field1', 'field2']

→ MyModel object to JSON
→ JSON to MyModel object


FIELD TYPES:

Automatically determined from model:
- CharField → "string"
- IntegerField → integer
- BooleanField → true/false
- ForeignKey → nested object or ID


NESTED SERIALIZERS:

class PropertySerializer(serializers.ModelSerializer):
    location = LocationSerializer(read_only=True)

Output:
{
    "title": "Villa",
    "location": {
        "name": "Miami",
        "city": "Miami"
    }
}

Without nested serializer:
{
    "title": "Villa",
    "location": 1  // Just the ID
}


SERIALIZER METHOD FIELD:

field_name = serializers.SerializerMethodField()

def get_field_name(self, obj):
    return calculated_value

→ Custom calculated field
→ Method name must be get_<field_name>


MANY=TRUE:

images = ImageSerializer(many=True)

→ Serializes list of objects
→ Returns array in JSON

Output:
{
    "images": [
        {"id": 1, ...},
        {"id": 2, ...}
    ]
}


READ_ONLY vs WRITE_ONLY:

read_only=True
→ Included in output
→ Ignored in input

write_only=True
→ Ignored in output
→ Required in input

Example: password field
password = serializers.CharField(write_only=True)
"""