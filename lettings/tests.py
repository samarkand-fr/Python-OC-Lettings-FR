"""
Unit and integration tests for the lettings application.

Tests models (Address, Letting), views (index, letting), and URL routing.
"""

from unittest.mock import patch
from django.test import TestCase, Client, override_settings
from django.urls import reverse, resolve
from lettings.models import Address, Letting
from lettings.views import index, letting


class LettingsModelTests(TestCase):
    """
    Test suite for Address and Letting models.
    """

    def setUp(self):
        """Create sample Address and Letting instances for model testing."""
        self.address = Address.objects.create(
            number=123,
            street='Main Street',
            city='Ocean City',
            state='MD',
            zip_code=21842,
            country_iso_code='USA'
        )
        self.letting = Letting.objects.create(
            title='Cozy Beach House',
            address=self.address
        )

    def test_address_str(self):
        """Test the string representation of an Address instance."""
        self.assertEqual(str(self.address), '123 Main Street')

    def test_address_verbose_name_plural(self):
        """Test that Address model plural name is correctly set to Addresses."""
        self.assertEqual(Address._meta.verbose_name_plural, 'Addresses')

    def test_letting_str(self):
        """Test the string representation of a Letting instance."""
        self.assertEqual(str(self.letting), 'Cozy Beach House')


class LettingsViewTests(TestCase):
    """
    Test suite for lettings views and URL resolution.
    """

    def setUp(self):
        """Set up test client and sample data for view tests."""
        self.client = Client()
        self.address = Address.objects.create(
            number=456,
            street='Sunset Boulevard',
            city='Los Angeles',
            state='CA',
            zip_code=90028,
            country_iso_code='USA'
        )
        self.letting = Letting.objects.create(
            title='Hollywood Loft',
            address=self.address
        )

    def test_lettings_index_url_resolves(self):
        """Test that the lettings index URL resolves to the index view."""
        match = resolve('/lettings/')
        self.assertEqual(match.func, index)

    def test_lettings_index_view(self):
        """Test the lettings index view status code, template, and content."""
        url = reverse('lettings:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lettings/index.html')
        self.assertContains(response, 'Hollywood Loft')

    def test_letting_detail_url_resolves(self):
        """Test that the letting detail URL resolves to the letting view."""
        match = resolve(f'/lettings/{self.letting.id}/')
        self.assertEqual(match.func, letting)

    def test_letting_detail_view_success(self):
        """Test the letting detail view status code, template, and content."""
        url = reverse('lettings:letting', kwargs={'letting_id': self.letting.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'lettings/letting.html')
        self.assertContains(response, 'Hollywood Loft')
        self.assertContains(response, 'Sunset Boulevard')

    @override_settings(DEBUG=False)
    def test_letting_detail_view_not_found(self):
        """Test that requesting a non-existent letting returns a 404 status."""
        url = reverse('lettings:letting', kwargs={'letting_id': 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')

    @patch('lettings.views.Letting.objects.all')
    def test_lettings_index_unexpected_error(self, mock_all):
        """Test that an unexpected exception in lettings index returns 500 page."""
        mock_all.side_effect = RuntimeError('Database failure')
        url = reverse('lettings:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 500)
        self.assertTemplateUsed(response, '500.html')

    @patch('lettings.views.Letting.objects.get')
    def test_letting_detail_view_unexpected_error(self, mock_get):
        """Test that an unexpected exception in letting view returns 500 page."""
        mock_get.side_effect = RuntimeError('Database failure')
        url = reverse('lettings:letting', kwargs={'letting_id': 1})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 500)
        self.assertTemplateUsed(response, '500.html')
