"""
Unit and integration tests for the oc_lettings_site application.

Tests the home page view, URL routing, custom 404 and 500 error handlers,
and the Sentry debug endpoint.
"""

from django.test import TestCase, Client, override_settings
from django.urls import reverse, resolve
from oc_lettings_site.views import index, handler404, handler500, sentry_debug


class OCLettingsSiteTests(TestCase):
    """
    Test suite for oc_lettings_site views and routing.
    """

    def setUp(self):
        """Set up test client before each test method."""
        self.client = Client()

    def test_index_url_resolves(self):
        """Test that the root URL resolves to the index view."""
        match = resolve('/')
        self.assertEqual(match.func, index)

    def test_index_view_status_and_template(self):
        """Test that the index view returns HTTP 200 and renders index.html."""
        url = reverse('index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Welcome to Holiday Homes')

    @override_settings(DEBUG=False)
    def test_404_page(self):
        """Test that requesting a non-existent URL returns 404 and renders 404.html."""
        response = self.client.get('/this-url-definitely-does-not-exist/')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')
        self.assertContains(response, '404 - Page Not Found', status_code=404)

    def test_handler404_direct_call(self):
        """Test direct invocation of the handler404 view."""
        from django.test import RequestFactory
        factory = RequestFactory()
        req = factory.get('/dummy-404/')
        self.assertEqual(handler404(req).status_code, 404)
        self.assertEqual(handler404(None).status_code, 404)

    def test_handler500_direct_call(self):
        """Test direct invocation of the handler500 view."""
        from django.test import RequestFactory
        factory = RequestFactory()
        req = factory.get('/dummy-500/')
        self.assertEqual(handler500(req).status_code, 500)
        self.assertEqual(handler500(None).status_code, 500)

    def test_sentry_debug_url_resolves(self):
        """Test that the sentry-debug URL resolves to sentry_debug view."""
        match = resolve('/sentry-debug/')
        self.assertEqual(match.func, sentry_debug)

    def test_sentry_debug_raises_zero_division(self):
        """Test that accessing sentry-debug triggers a ZeroDivisionError."""
        with self.assertRaises(ZeroDivisionError):
            self.client.get('/sentry-debug/')
