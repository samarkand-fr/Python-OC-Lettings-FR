"""
Views for the oc_lettings_site application.

This module provides the main index view for the site's home page,
custom HTTP 404 and 500 error handlers, and a test view to verify
Sentry error tracking and logging.
"""

import logging
from django.shortcuts import render

logger = logging.getLogger(__name__)


def index(request):
    """
    Display the home page of the Holiday Homes site.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: Rendered home page, or 500 page on failure.
    """
    try:
        logger.info("Accessed home page index view.")
        return render(request, 'index.html')
    except Exception as exc:
        logger.error("Failed to render home page: %s", exc, exc_info=True)
        return render(request, '500.html', status=500)


def handler404(request, exception=None):
    """
    Render custom 404 Not Found error page and log the event.

    Args:
        request (HttpRequest): The incoming HTTP request.
        exception (Exception, optional): The exception that triggered the 404 error.

    Returns:
        HttpResponseNotFound: Rendered 404 error page with HTTP status 404.
    """
    path = request.path if request else 'unknown'
    logger.warning("404 error encountered for path: %s", path)
    return render(request, '404.html', status=404)


def handler500(request):
    """
    Render custom 500 Internal Server Error page and log the event.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponseServerError: Rendered 500 error page with HTTP status 500.
    """
    path = request.path if request else 'unknown'
    logger.error("500 internal server error encountered for path: %s", path)
    return render(request, '500.html', status=500)


def sentry_debug(request):
    """
    Trigger an intentional division by zero error to test Sentry error tracking.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Raises:
        ZeroDivisionError: Always raised to trigger Sentry event capture.
    """
    logger.info("Triggering intentional error for Sentry verification.")
    division_by_zero = 1 / 0
    return division_by_zero
