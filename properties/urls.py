"""
Property URLs

WHAT THIS FILE DOES:
- Maps URLs to view functions
- Defines URL patterns for property pages

TOPICS TO LEARN:
- URL patterns
- URL parameters
- Named URLs
- URL namespacing
"""

from django.urls import path
from . import views

# Namespace for these URLs
app_name = 'properties'
# EXPLANATION:
# - app_name creates a namespace
# - Access URLs like: {% url 'properties:home' %}
# - Prevents name conflicts with other apps


urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    # EXPLANATION:
    # - '' = Root URL (/)
    # - views.home = Call home() function in views.py
    # - name='home' = Name for reverse URL lookup
    # URL: http://127.0.0.1:8000/
    
    
    # Property list page
    path('properties/', views.property_list, name='property_list'),
    # EXPLANATION:
    # - 'properties/' = /properties/ URL
    # - views.property_list = Call property_list() function
    # - name='property_list' = Named URL
    # URL: http://127.0.0.1:8000/properties/
    # URL with filter: http://127.0.0.1:8000/properties/?location=Miami
    
    
    # Property detail page
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
    # EXPLANATION:
    # - 'property/<int:pk>/' = /property/1/, /property/2/, etc.
    # - <int:pk> = Capture integer as 'pk' parameter
    # - views.property_detail = Call property_detail(request, pk) function
    # - name='property_detail' = Named URL
    # URL: http://127.0.0.1:8000/property/1/
    # URL: http://127.0.0.1:8000/property/5/
]


"""
URL PATTERNS EXPLAINED:

path(route, view, kwargs=None, name=None)

- route = URL pattern string
- view = View function to call
- name = Name for reverse URL lookup


URL PARAMETERS:

<type:name>
- Captures part of URL and passes to view
- Types: int, str, slug, uuid, path

Examples:
path('product/<int:id>/', view)
  → /product/5/ → view(request, id=5)

path('category/<str:name>/', view)
  → /category/electronics/ → view(request, name='electronics')

path('user/<slug:username>/', view)
  → /user/john-doe/ → view(request, username='john-doe')


NAMED URLS:

Instead of hardcoding URLs:
<a href="/properties/">Properties</a>  ❌

Use named URLs:
<a href="{% url 'properties:property_list' %}">Properties</a>  ✅

In Python:
from django.urls import reverse
url = reverse('properties:property_list')  # Returns '/properties/'


URL NAMESPACING:

app_name = 'properties'

Access in templates:
{% url 'properties:home' %}
{% url 'properties:property_list' %}
{% url 'properties:property_detail' pk=1 %}

Access in Python:
reverse('properties:home')
reverse('properties:property_detail', kwargs={'pk': 1})


URL PATTERNS WITH PARAMETERS:

path('property/<int:pk>/', view, name='property_detail')

In template:
{% url 'properties:property_detail' pk=property.id %}
→ /property/5/

{% url 'properties:property_detail' property.id %}
→ /property/5/

In Python:
reverse('properties:property_detail', kwargs={'pk': 5})
→ '/property/5/'


QUERY PARAMETERS:

Query parameters are NOT defined in URLs:
/properties/?location=Miami&bedrooms=3

They're accessed in views:
location = request.GET.get('location')
bedrooms = request.GET.get('bedrooms')

In templates:
<a href="{% url 'properties:property_list' %}?location=Miami">Miami</a>
"""