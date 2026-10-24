"""
Views for the lettings application.

This module provides views to list all available lettings
and to display the detail of a single letting, with structured try/except
error handling and logging.
"""

import logging
from django.shortcuts import render
from .models import Letting

logger = logging.getLogger(__name__)


def index(request):
    """
    Display a list of all available lettings.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: Rendered page with the list of lettings,
                      or 500 error page if an unexpected error occurs.
    """
    try:
        lettings_list = Letting.objects.all()
        logger.info("Retrieved %d lettings for listing view.", lettings_list.count())
        context = {'lettings_list': lettings_list}
        return render(request, 'lettings/index.html', context)
    except Exception as exc:
        logger.error("Failed to retrieve lettings list: %s", exc, exc_info=True)
        return render(request, '500.html', status=500)


def letting(request, letting_id):
    """
    Display the detail page for a single letting.

    Catches DoesNotExist exceptions to return a 404 page,
    and unexpected exceptions to log and return a 500 error page.

    Args:
        request (HttpRequest): The incoming HTTP request.
        letting_id (int): The primary key of the letting to display.

    Returns:
        HttpResponse: Rendered page with letting title and address,
                      or 404/500 error page if an error occurs.
    """
    try:
        letting_obj = Letting.objects.get(id=letting_id)
        logger.info(
            "Retrieved letting ID %d: '%s' at '%s'.",
            letting_id,
            letting_obj.title,
            letting_obj.address
        )
        context = {
            'title': letting_obj.title,
            'address': letting_obj.address,
        }
        return render(request, 'lettings/letting.html', context)
    except Letting.DoesNotExist:
        logger.warning("Letting with ID %d not found.", letting_id)
        return render(request, '404.html', status=404)
    except Exception as exc:
        logger.error(
            "Unexpected error retrieving letting ID %d: %s",
            letting_id,
            exc,
            exc_info=True
        )
        return render(request, '500.html', status=500)
