"""
Views for the oc_lettings_site application.

This module provides the main index view for the site's home page.
"""

from django.shortcuts import render


def index(request):
    """
    Display the home page of the Holiday Homes site.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: Rendered home page.
    """
    return render(request, 'index.html')
