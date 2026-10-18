"""
URL configuration for the profiles application.

Defines URL patterns for listing all profiles and viewing a single profile.
The app namespace is 'profiles'.
"""

from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:username>/', views.profile, name='profile'),
]
