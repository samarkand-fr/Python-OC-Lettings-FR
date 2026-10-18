"""
URL configuration for the lettings application.

Defines URL patterns for listing all lettings and viewing a single letting.
The app namespace is 'lettings'.
"""

from django.urls import path
from . import views

app_name = 'lettings'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:letting_id>/', views.letting, name='letting'),
]
