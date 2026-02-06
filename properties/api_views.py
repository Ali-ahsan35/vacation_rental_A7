"""
API Views

WHAT THIS FILE DOES:
- Handles API requests
- Returns JSON responses
- Implements autocomplete endpoint

TOPICS TO LEARN:
- Django REST Framework ViewSets
- API endpoints
- JSON responses
- Query filtering
"""

from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from locations.models import Location
from properties.models import Property
# Import serializers from the file we'll create
from .api_serializers import (
    LocationSerializer,
    PropertyListSerializer,
    PropertyDetailSerializer
)


# ==================== LOCATION VIEWSET ====================

class LocationViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for locations
    
    ENDPOINTS:
    GET /api/locations/ - List all locations
    GET /api/locations/1/ - Get location detail
    GET /api/locations/autocomplete/?q=Miami - Autocomplete search
    """
    
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    # EXPLANATION:
    # - queryset = What data to show
    # - serializer_class = How to convert to JSON
    
    # Enable filtering and search
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'city', 'state']
    ordering_fields = ['name', 'city']
    ordering = ['name']  # Default ordering
    
    
    @action(detail=False, methods=['get'])
    def autocomplete(self, request):
        """
        Autocomplete endpoint for location search
        
        WHAT THIS DOES:
        - Searches locations by name, city, or state
        - Returns top 5 matches
        - Used for search autocomplete on frontend
        
        ENDPOINT: GET /api/locations/autocomplete/?q=Miami
        
        Example request:
        GET /api/locations/autocomplete/?q=mia
        
        Example response:
        [
            {
                "id": 1,
                "name": "Miami Beach",
                "city": "Miami",
                "state": "Florida",
                "country": "USA"
            },
            {
                "id": 2,
                "name": "Miami Downtown",
                "city": "Miami",
                "state": "Florida",
                "country": "USA"
            }
        ]
        """
        
        # Get search query from URL parameter
        query = request.query_params.get('q', '').strip()
        # EXPLANATION:
        # - request.query_params = URL parameters (same as request.GET)
        # - .get('q', '') = Get 'q' parameter, default to empty
        # Example: /autocomplete/?q=miami → query = "miami"
        
        # Return empty list if no query
        if not query:
            return Response([])
        
        # Search for locations
        locations = Location.objects.filter(
            Q(name__icontains=query) |
            Q(city__icontains=query) |
            Q(state__icontains=query)
        )[:5]  # Limit to 5 results
        # EXPLANATION:
        # - Q() = Complex query
        # - | = OR operator
        # - icontains = Case-insensitive contains
        # - [:5] = Limit to 5 results (LIMIT 5 in SQL)
        
        # Serialize and return
        serializer = self.get_serializer(locations, many=True)
        return Response(serializer.data)
        # EXPLANATION:
        # - self.get_serializer() = Get LocationSerializer
        # - many=True = Multiple objects
        # - serializer.data = Convert to JSON
        # - Response() = Return JSON response


# ==================== PROPERTY VIEWSET ====================

class PropertyViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for properties
    
    ENDPOINTS:
    GET /api/properties/ - List all properties
    GET /api/properties/1/ - Get property detail
    GET /api/properties/?location=Miami - Filter by location
    GET /api/properties/?bedrooms=3 - Filter by bedrooms
    """
    
    queryset = Property.objects.select_related('location').prefetch_related('images')
    # EXPLANATION:
    # - select_related('location') = Join with Location (optimization)
    # - prefetch_related('images') = Load images (optimization)
    
    # Enable filtering and search
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['location', 'property_type', 'bedrooms', 'is_available']
    search_fields = ['title', 'description', 'location__name']
    ordering_fields = ['price_per_night', 'created_at', 'bedrooms']
    ordering = ['-created_at']  # Default: newest first
    
    
    def get_serializer_class(self):
        """
        Return appropriate serializer based on action
        
        WHAT THIS DOES:
        - List view → PropertyListSerializer (less data)
        - Detail view → PropertyDetailSerializer (full data)
        """
        if self.action == 'retrieve':
            # Detail view (GET /api/properties/1/)
            return PropertyDetailSerializer
        # List view (GET /api/properties/)
        return PropertyListSerializer
    
    
    def get_queryset(self):
        """
        Filter queryset by location name if provided
        
        WHAT THIS DOES:
        Allows filtering by location name in URL
        
        Example: GET /api/properties/?location=Miami
        """
        queryset = super().get_queryset()
        
        # Get location parameter
        location_name = self.request.query_params.get('location', None)
        
        if location_name:
            # Filter by location name or city
            queryset = queryset.filter(
                Q(location__name__icontains=location_name) |
                Q(location__city__icontains=location_name)
            )
        
        return queryset


"""
VIEWSETS EXPLAINED:

ViewSet = Class that handles API endpoints

class MyViewSet(viewsets.ModelViewSet):
    queryset = MyModel.objects.all()
    serializer_class = MySerializer

Automatically creates:
- GET /api/mymodel/ - List
- POST /api/mymodel/ - Create
- GET /api/mymodel/1/ - Detail
- PUT /api/mymodel/1/ - Update
- DELETE /api/mymodel/1/ - Delete


READONLY VIEWSET:

viewsets.ReadOnlyModelViewSet
→ Only GET requests (list and detail)
→ No POST, PUT, DELETE

Good for: Public APIs, read-only data


CUSTOM ACTIONS:

@action(detail=False, methods=['get'])
def custom_endpoint(self, request):
    return Response({'message': 'Custom!'})

- detail=False → /api/model/custom_endpoint/
- detail=True → /api/model/1/custom_endpoint/
- methods = HTTP methods allowed


FILTER BACKENDS:

DjangoFilterBackend:
→ Filter by exact field values
→ /api/properties/?bedrooms=3&property_type=Villa

SearchFilter:
→ Search across multiple fields
→ /api/properties/?search=beach

OrderingFilter:
→ Sort results
→ /api/properties/?ordering=price_per_night
→ /api/properties/?ordering=-created_at (descending)


QUERYSET OPTIMIZATION:

select_related('foreign_key_field'):
→ JOIN in SQL
→ One query instead of many
→ Use for ForeignKey

prefetch_related('reverse_foreign_key'):
→ Separate query, joined in Python
→ Use for reverse ForeignKey (one-to-many)

Example:
Property.objects.select_related('location').prefetch_related('images')
→ Gets properties, locations, and images efficiently


REQUEST OBJECT IN DRF:

request.query_params = URL parameters
request.data = POST/PUT data (JSON)
request.user = Current user
request.method = HTTP method


RESPONSE OBJECT:

Response(data, status=200)
→ Returns JSON response
→ Automatically serializes data

return Response({'message': 'Success'})
return Response(serializer.data)
return Response([], status=404)
"""