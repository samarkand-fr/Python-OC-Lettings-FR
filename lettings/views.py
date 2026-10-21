"""
Views for the lettings application.

This module provides views to list all available lettings
and to display the detail of a single letting.
"""

from django.shortcuts import render, get_object_or_404
from .models import Letting


def index(request):
    """
    Display a list of all available lettings.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: Rendered page with the list of all lettings.
    """
    lettings_list = Letting.objects.all()
    context = {'lettings_list': lettings_list}
    return render(request, 'lettings/index.html', context)


def letting(request, letting_id):
    """
    Display the detail page for a single letting.

    Args:
        request (HttpRequest): The incoming HTTP request.
        letting_id (int): The primary key of the letting to display.

    Returns:
        HttpResponse: Rendered page with letting title and address details.
    """
    letting = get_object_or_404(Letting, id=letting_id)
    context = {
        'title': letting.title,
        'address': letting.address,
    }
    return render(request, 'lettings/letting.html', context)
