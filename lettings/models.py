"""
Models for the lettings application.

This module defines the Address and Letting models used to represent
rental listings and their associated physical addresses.
"""

from django.db import models
from django.core.validators import MaxValueValidator, MinLengthValidator


class Address(models.Model):
    """
    Represents a physical address for a rental property.

    Attributes:
        number (int): Street number (max 9999).
        street (str): Street name (max 64 characters).
        city (str): City name (max 64 characters).
        state (str): Two-letter state code.
        zip_code (int): ZIP code (max 99999).
        country_iso_code (str): Three-letter ISO country code.
    """

    number = models.PositiveIntegerField(validators=[MaxValueValidator(9999)])
    street = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=2, validators=[MinLengthValidator(2)])
    zip_code = models.PositiveIntegerField(validators=[MaxValueValidator(99999)])
    country_iso_code = models.CharField(max_length=3, validators=[MinLengthValidator(3)])

    class Meta:
        """Meta options for the Address model."""

        verbose_name_plural = 'Addresses'

    def __str__(self):
        """Return string representation of the address."""
        return f'{self.number} {self.street}'


class Letting(models.Model):
    """
    Represents a rental letting listing.

    Attributes:
        title (str): Title of the letting (max 256 characters).
        address (Address): One-to-one relation to an Address instance.
    """

    title = models.CharField(max_length=256)
    address = models.OneToOneField(Address, on_delete=models.CASCADE)

    def __str__(self):
        """Return string representation of the letting."""
        return self.title
