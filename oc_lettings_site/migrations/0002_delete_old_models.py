"""
Migration to delete legacy models from oc_lettings_site.

Address, Letting, and Profile models have been migrated to the
lettings and profiles applications respectively.
"""

from django.db import migrations


class Migration(migrations.Migration):
    """Migration deleting obsolete tables from oc_lettings_site."""

    dependencies = [
        ('oc_lettings_site', '0001_initial'),
        ('lettings', '0002_copy_lettings_data'),
        ('profiles', '0002_copy_profiles_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='letting',
            name='address',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.DeleteModel(
            name='Address',
        ),
        migrations.DeleteModel(
            name='Letting',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
