"""
Pytest configuration for the oc_lettings_site project.

Initializes Django settings and instruments the test environment
when pytest-django is not installed.
"""

import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oc_lettings_site.settings')
os.environ.setdefault('SECRET_KEY', 'test-secret-key-for-test-suite-runs')
os.environ['SENTRY_DSN'] = ''

if not settings.configured:
    django.setup()


def pytest_configure(config):
    """
    Configure pytest hook. If pytest-django plugin is not present,
    initialize the Django test environment for template tracking.
    """
    if not config.pluginmanager.hasplugin('django'):
        from django.test.utils import setup_test_environment
        setup_test_environment()
