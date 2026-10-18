"""
Root URL configuration for the oc_lettings_site project.

Routes requests to the home page, the admin interface,
and the lettings and profiles applications.
"""

from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lettings/', include('lettings.urls')),
    path('profiles/', include('profiles.urls')),
    path('admin/', admin.site.urls),
]
