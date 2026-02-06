"""
Main URL Configuration

WHAT THIS FILE DOES:
- Routes URLs to different parts of the application
- Connects admin panel
- Serves media files in development

TOPICS TO LEARN:
- URL routing
- URL patterns
- Include other URL files
- Static and media file serving
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),

]

if settings.DEBUG:
    # Only serve media files when DEBUG = True (development)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


