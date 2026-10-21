"""
Unit and integration tests for the profiles application.

Tests models (Profile), views (index, profile), and URL routing.
"""

from django.test import TestCase, Client, override_settings
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from profiles.models import Profile
from profiles.views import index, profile


class ProfilesModelTests(TestCase):
    """
    Test suite for the Profile model.
    """

    def setUp(self):
        """Create a sample User and Profile instance for model testing."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            favorite_city='Paris'
        )

    def test_profile_str(self):
        """Test the string representation of a Profile instance."""
        self.assertEqual(str(self.profile), 'testuser')


class ProfilesViewTests(TestCase):
    """
    Test suite for profiles views and URL resolution.
    """

    def setUp(self):
        """Set up test client and sample data for view tests."""
        self.client = Client()
        self.user = User.objects.create_user(
            username='janedoe',
            first_name='Jane',
            last_name='Doe',
            email='jane@example.com',
            password='password123'
        )
        self.profile = Profile.objects.create(
            user=self.user,
            favorite_city='Tokyo'
        )

    def test_profiles_index_url_resolves(self):
        """Test that the profiles index URL resolves to the index view."""
        match = resolve('/profiles/')
        self.assertEqual(match.func, index)

    def test_profiles_index_view(self):
        """Test the profiles index view status code, template, and content."""
        url = reverse('profiles:index')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/index.html')
        self.assertContains(response, 'janedoe')

    def test_profile_detail_url_resolves(self):
        """Test that the profile detail URL resolves to the profile view."""
        match = resolve(f'/profiles/{self.user.username}/')
        self.assertEqual(match.func, profile)

    def test_profile_detail_view_success(self):
        """Test the profile detail view status code, template, and content."""
        url = reverse('profiles:profile', kwargs={'username': self.user.username})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')
        self.assertContains(response, 'janedoe')
        self.assertContains(response, 'Tokyo')
        self.assertContains(response, 'Jane')
        self.assertContains(response, 'Doe')
        self.assertContains(response, 'jane@example.com')

    @override_settings(DEBUG=False)
    def test_profile_detail_view_not_found(self):
        """Test that requesting a non-existent profile returns a 404 status."""
        url = reverse('profiles:profile', kwargs={'username': 'nonexistentuser'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, '404.html')
