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

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    
    # Property list page
    path('properties/', views.property_list, name='property_list'),

    # Property detail page
    path('property/<int:pk>/', views.property_detail, name='property_detail'),
]