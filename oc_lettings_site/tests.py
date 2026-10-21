"""
Unit and integration tests for the oc_lettings_site application.

Tests the home page view, URL routing, and custom 404 and 500 error handlers.
"""

from django.test import TestCase, Client, override_settings
from django.urls import reverse, resolve
from oc_lettings_site.views import index, handler404, handler500


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
        response = handler404(None)
        self.assertEqual(response.status_code, 404)

    def test_handler500_direct_call(self):
        """Test direct invocation of the handler500 view."""
        response = handler500(None)
        self.assertEqual(response.status_code, 500)
