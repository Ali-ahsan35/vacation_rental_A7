"""
Main URL Configuration

WHAT THIS FILE DOES:
- Routes URLs to different parts of the application
- Includes URLs from other apps
- Serves media files in development
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),
    # URL: http://127.0.0.1:8000/admin/
    
    # API endpoints
    path('api/', include('properties.api_urls')),
    # - 'api/' prefix for all API URLs
    # - Includes all URLs from properties/api_urls.py
    # - /api/locations/ → location list
    # - /api/locations/autocomplete/?q=Miami → autocomplete
    # - /api/properties/ → property list
    # - /api/properties/1/ → property detail
    
    # Include property URLs (home, list, detail)
    path('', include('properties.urls')),
    # - '' means no prefix
    # - Includes all URLs from properties/urls.py
    # - / → home page
    # - /properties/ → property list
    # - /property/1/ → property detail
]


# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # - Only when DEBUG = True (development)
    # - Serves uploaded images
    # - /media/property_images/image.jpg


"""
INCLUDE EXPLAINED:

path('prefix/', include('app.urls'))
→ Includes all URLs from app/urls.py with prefix

Examples:

path('', include('properties.urls'))
  properties/urls.py has: path('properties/', view)
  → Final URL: /properties/

path('api/', include('api.urls'))
  api/urls.py has: path('locations/', view)
  → Final URL: /api/locations/


URL RESOLUTION ORDER:

Django checks URLs from top to bottom:
1. path('admin/', ...)  → Matches /admin/
2. path('', include(...))  → Matches everything else

Be careful with order!
❌ Wrong:
path('', include(...))  # Catches everything
path('admin/', ...)  # Never reached!

✅ Correct:
path('admin/', ...)  # Specific first
path('', include(...))  # General last
"""