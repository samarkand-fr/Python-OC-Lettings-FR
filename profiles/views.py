"""
Views for the profiles application.

This module provides views to list all user profiles
and to display the detail of a single profile.
"""

from django.shortcuts import render
from .models import Profile


def index(request):
    """
    Display a list of all user profiles.

    Args:
        request (HttpRequest): The incoming HTTP request.

    Returns:
        HttpResponse: Rendered page with the list of all profiles.
    """
    profiles_list = Profile.objects.all()
    context = {'profiles_list': profiles_list}
    return render(request, 'profiles/index.html', context)


def profile(request, username):
    """
    Display the detail page for a single user profile.

    Args:
        request (HttpRequest): The incoming HTTP request.
        username (str): The username of the profile to display.

    Returns:
        HttpResponse: Rendered page with the user's profile details.
    """
    profile = Profile.objects.get(user__username=username)
    context = {'profile': profile}
    return render(request, 'profiles/profile.html', context)
