"""
Views for the oc_lettings_site application.

This module provides the main index view for the site's home page
as well as custom HTTP 404 and 500 error handlers.
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


def handler404(request, exception=None):
    """
    Render custom 404 Not Found error page.

    Args:
        request (HttpRequest): The incoming HTTP request.
        exception (Exception, optional): The exception that triggered the 404 error.

    Returns:
        HttpResponseNotFound: Rendered 404 error page with HTTP status 404.
    """
    return render(request, '404.html', status=404)


def handler500(request):
    """
    Render custom 500 Internal Server Error page.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponseServerError: Rendered 500 error page with HTTP status 500.
    """
    return render(request, '500.html', status=500)
