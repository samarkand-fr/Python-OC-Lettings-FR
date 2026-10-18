"""
Models for the profiles application.

This module defines the Profile model, which extends Django's built-in
User model with additional information such as a favorite city.
"""

from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    """
    Extends the built-in Django User model with additional profile information.

    Attributes:
        user (User): One-to-one relation to Django's User model.
        favorite_city (str): The user's favorite city (optional, max 64 characters).
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_city = models.CharField(max_length=64, blank=True)

    def __str__(self):
        """Return string representation of the profile (username)."""
        return self.user.username
