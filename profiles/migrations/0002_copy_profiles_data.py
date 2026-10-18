"""
Data migration for the profiles application.

Copies Profile data from the legacy oc_lettings_site table
to the new profiles app table using Django's ORM (no raw SQL).
"""

from django.db import migrations


def copy_profiles_data(apps, schema_editor):
    """
    Copy Profile records from oc_lettings_site to profiles app.

    Args:
        apps: Django app registry providing access to historical models.
        schema_editor: Database schema editor (unused but required by Django).
    """
    OldProfile = apps.get_model('oc_lettings_site', 'Profile')
    NewProfile = apps.get_model('profiles', 'Profile')

    for old_profile in OldProfile.objects.all():
        NewProfile.objects.create(
            id=old_profile.id,
            user_id=old_profile.user_id,
            favorite_city=old_profile.favorite_city,
        )


def reverse_copy_profiles_data(apps, schema_editor):
    """
    Reverse the data copy by deleting all records in the new profiles table.

    Args:
        apps: Django app registry providing access to historical models.
        schema_editor: Database schema editor (unused but required by Django).
    """
    NewProfile = apps.get_model('profiles', 'Profile')
    NewProfile.objects.all().delete()


class Migration(migrations.Migration):
    """Migration to copy data from oc_lettings_site to profiles app."""

    dependencies = [
        ('profiles', '0001_initial_profiles'),
        ('oc_lettings_site', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(copy_profiles_data, reverse_copy_profiles_data),
    ]
