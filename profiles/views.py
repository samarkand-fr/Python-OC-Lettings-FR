"""
Views for the profiles application.

This module provides views to list all user profiles
and to display the detail of a single profile, with structured try/except
error handling and logging.
"""

import logging
from django.shortcuts import render
from .models import Profile

logger = logging.getLogger(__name__)


def index(request):
    """
    Display a list of all user profiles.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: Rendered page with the list of profiles,
                      or 500 error page if an unexpected error occurs.
    """
    try:
        profiles_list = Profile.objects.all()
        logger.info("Retrieved %d profiles for listing view.", profiles_list.count())
        context = {'profiles_list': profiles_list}
        return render(request, 'profiles/index.html', context)
    except Exception as exc:
        logger.error("Failed to retrieve profiles list: %s", exc, exc_info=True)
        return render(request, '500.html', status=500)


def profile(request, username):
    """
    Display the detail page for a single user profile.

    Catches DoesNotExist exceptions to return a 404 page,
    and unexpected exceptions to log and return a 500 error page.

    Args:
        request (HttpRequest): The incoming HTTP request.
        username (str): The username of the profile to display.

    Returns:
        HttpResponse: Rendered page with profile details,
                      or 404/500 error page if an error occurs.
    """
    try:
        profile_obj = Profile.objects.get(user__username=username)
        logger.info(
            "Retrieved profile for user '%s' (favorite city: '%s').",
            username,
            profile_obj.favorite_city
        )
        context = {'profile': profile_obj}
        return render(request, 'profiles/profile.html', context)
    except Profile.DoesNotExist:
        logger.warning("Profile for user '%s' not found.", username)
        return render(request, '404.html', status=404)
    except Exception as exc:
        logger.error(
            "Unexpected error retrieving profile for user '%s': %s",
            username,
            exc,
            exc_info=True
        )
        return render(request, '500.html', status=500)
