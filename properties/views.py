"""
Property Views

WHAT THIS FILE DOES:
- Handles web page requests
- Renders HTML templates
- Passes data to templates
- Implements pagination and filtering

TOPICS TO LEARN:
- Function-based views
- QuerySets
- Pagination
- Context data
- Template rendering
"""

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Property
from locations.models import Location


def home(request):
    """
    Home page with search form
    
    Renders the homepage with a search input
    
    URL: /
    TEMPLATE: templates/properties/home.html
    """
    return render(request, 'properties/home.html')



def property_list(request):
    """
    Property list page with location filtering and pagination
    
    - Shows all available properties
    - Filters by location if query parameter present
    - Paginates results (9 per page)
    
    URL: /properties/
    URL with filter: /properties/?location=Miami
    TEMPLATE: templates/properties/property_list.html
    """
    
    # GET ALL PROPERTIES
    # Start with all properties that are available
    properties = Property.objects.select_related('location').prefetch_related('images').filter(is_available=True)
    # EXPLANATION:
    # - Property.objects = Manager for querying database
    # - select_related('location') = Join with Location table (optimization)
    # - prefetch_related('images') = Load related images (optimization)
    # - filter(is_available=True) = Only show available properties
    
    
    # FILTER BY LOCATION
    # Get the 'location' query parameter from URL
    location_query = request.GET.get('location', '').strip()
    # EXPLANATION:
    # - request.GET = Dictionary of URL parameters
    # - .get('location', '') = Get 'location' parameter, default to empty string
    # - .strip() = Remove whitespace
    # Example: /properties/?location=Miami → location_query = "Miami"
    
    if location_query:
        # Filter properties by location name, city, or state
        properties = properties.filter(
            Q(location__name__icontains=location_query) |
            Q(location__city__icontains=location_query) |
            Q(location__state__icontains=location_query)
        )
        # EXPLANATION:
        # - Q() = Complex query object
        # - | = OR operator
        # - location__name__icontains = Case-insensitive contains
        # - This searches in location name, city, AND state
        # Example: "Miami" matches "Miami Beach" or city="Miami"
    
    
    # PAGINATION
    # Create paginator (9 properties per page)
    paginator = Paginator(properties, 9)
    # EXPLANATION:
    # - Paginator divides queryset into pages
    # - 9 properties per page
    
    # Get the page number from URL
    page_number = request.GET.get('page')
    
    # Get the specific page
    page_obj = paginator.get_page(page_number)

        
    # PREPARE CONTEXT DATA
    context = {
        'page_obj': page_obj,                    # Page object with properties
        'location_query': location_query,        # Search query (for form)
        'total_properties': properties.count(),  # Total count of properties
    }
    
    # RENDER TEMPLATE
    return render(request, 'properties/property_list.html', context)


def property_detail(request, pk):
    """
    Property detail page showing all information and images
    
    WHAT THIS DOES:
    - Shows single property with all details
    - Shows all images in carousel
    - Shows amenities list
    
    URL: /property/<id>/
    Example: /property/1/
    TEMPLATE: templates/properties/property_detail.html
    """
    
    # GET PROPERTY OR 404
    property_obj = get_object_or_404(
        Property.objects.select_related('location').prefetch_related('images'),
        pk=pk
    )

    
    # PREPARE CONTEXT DATA
    context = {
        'property': property_obj,
    }
    
    # RENDER TEMPLATE
    return render(request, 'properties/property_detail.html', context)


"""
VIEWS EXPLAINED:

A view is a Python function that:
1. Takes a request
2. Processes it (query database, etc.)
3. Returns an HTTP response (usually HTML)

def view_name(request):
    # Process request
    data = Model.objects.all()
    
    # Prepare context
    context = {'data': data}
    
    # Render template
    return render(request, 'template.html', context)


REQUEST OBJECT:

request.GET = URL parameters (?location=Miami)
request.POST = Form data (submitted forms)
request.user = Current logged-in user
request.method = 'GET', 'POST', etc.


QUERYSETS:

Property.objects.all() = All properties
Property.objects.filter(bedrooms=3) = Filter
Property.objects.get(pk=1) = Get one object
Property.objects.exclude(is_available=False) = Exclude
Property.objects.order_by('-price') = Order by price descending


QUERY OPTIMIZATIONS:

select_related('location'):
- For ForeignKey relationships
- Loads related object in same query
- Use when you WILL access the related object

prefetch_related('images'):
- For reverse ForeignKey (one-to-many)
- Loads related objects in separate query
- Use when you WILL access multiple related objects


Q OBJECTS (Complex Queries):

Q(field__lookup=value)
- Allows OR, AND, NOT logic

Examples:
Q(city='Miami') | Q(city='Aspen')  # OR
Q(bedrooms=3) & Q(bathrooms__gte=2)  # AND
~Q(is_available=False)  # NOT

Field lookups:
- exact = Exact match
- iexact = Case-insensitive exact
- contains = Contains
- icontains = Case-insensitive contains
- gt = Greater than
- gte = Greater than or equal
- lt = Less than
- lte = Less than or equal


PAGINATION:

from django.core.paginator import Paginator

paginator = Paginator(queryset, per_page)
page = paginator.get_page(page_number)

page.object_list = Items on this page
page.number = Current page number
page.has_previous() = Is there a previous page?
page.has_next() = Is there a next page?
page.previous_page_number() = Previous page number
page.next_page_number() = Next page number


RENDER FUNCTION:

render(request, template, context, content_type, status)

- request = HTTP request object (required)
- template = Path to template file (required)
- context = Dictionary of data for template
- Returns HttpResponse with rendered HTML


GET_OBJECT_OR_404:

get_object_or_404(Model, pk=1)

- Try to get object
- If doesn't exist, return 404 page
- Better than try/except for user-facing views
"""