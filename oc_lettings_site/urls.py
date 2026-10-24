"""
Root URL configuration for the oc_lettings_site project.

Routes requests to the home page, the admin interface,
the lettings and profiles applications, and a Sentry debug endpoint.
Also defines custom HTTP 404 and 500 error handlers.
"""

from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('lettings/', include('lettings.urls')),
    path('profiles/', include('profiles.urls')),
    path('admin/', admin.site.urls),
    path('sentry-debug/', views.sentry_debug, name='sentry_debug'),
]

handler404 = 'oc_lettings_site.views.handler404'
handler500 = 'oc_lettings_site.views.handler500'
