"""
Data migration for the lettings application.

Copies Address and Letting data from the legacy oc_lettings_site tables
to the new lettings app tables using Django's ORM (no raw SQL).
"""

from django.db import migrations


def copy_lettings_data(apps, schema_editor):
    """
    Copy Address and Letting records from oc_lettings_site to lettings app.

    Args:
        apps: Django app registry providing access to historical models.
        schema_editor: Database schema editor (unused but required by Django).
    """
    OldAddress = apps.get_model('oc_lettings_site', 'Address')
    OldLetting = apps.get_model('oc_lettings_site', 'Letting')
    NewAddress = apps.get_model('lettings', 'Address')
    NewLetting = apps.get_model('lettings', 'Letting')

    # Copy addresses and keep a mapping from old id to new instance
    address_map = {}
    for old_address in OldAddress.objects.all():
        new_address = NewAddress.objects.create(
            id=old_address.id,
            number=old_address.number,
            street=old_address.street,
            city=old_address.city,
            state=old_address.state,
            zip_code=old_address.zip_code,
            country_iso_code=old_address.country_iso_code,
        )
        address_map[old_address.id] = new_address

    # Copy lettings referencing the new addresses
    for old_letting in OldLetting.objects.all():
        NewLetting.objects.create(
            id=old_letting.id,
            title=old_letting.title,
            address=address_map[old_letting.address_id],
        )


def reverse_copy_lettings_data(apps, schema_editor):
    """
    Reverse the data copy by deleting all records in new lettings tables.

    Args:
        apps: Django app registry providing access to historical models.
        schema_editor: Database schema editor (unused but required by Django).
    """
    NewLetting = apps.get_model('lettings', 'Letting')
    NewAddress = apps.get_model('lettings', 'Address')
    NewLetting.objects.all().delete()
    NewAddress.objects.all().delete()


class Migration(migrations.Migration):
    """Migration to copy data from oc_lettings_site to lettings app."""

    dependencies = [
        ('lettings', '0001_initial_lettings'),
        ('oc_lettings_site', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(copy_lettings_data, reverse_copy_lettings_data),
    ]
