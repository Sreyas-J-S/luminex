"""
Accounts app tests: registration, login, open redirect prevention, logout, profile.
"""
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse


class AuthAndRedirectTest(TestCase):
    def setUp(self):
        self.username = "testuser"
        self.password = "ComplexPass123!"
        self.user = User.objects.create_user(
            username=self.username,
            email="testuser@example.com",
            password=self.password,
            first_name="Test",
            last_name="User"
        )

    def test_ordinary_login_redirects_to_home(self):
        response = self.client.post(reverse('accounts:login'), {
            'username': self.username,
            'password': self.password,
        })
        self.assertRedirects(response, reverse('store:home'))

    def test_valid_internal_redirect(self):
        profile_url = reverse('accounts:profile')
        response = self.client.post(f"{reverse('accounts:login')}?next={profile_url}", {
            'username': self.username,
            'password': self.password,
        })
        self.assertRedirects(response, profile_url)

    def test_open_redirect_external_url_blocked(self):
        # External URL must NOT be followed; should safely fall back to store:home
        response = self.client.post(f"{reverse('accounts:login')}?next=https://evil.com", {
            'username': self.username,
            'password': self.password,
        })
        self.assertRedirects(response, reverse('store:home'))

    def test_open_redirect_protocol_relative_url_blocked(self):
        # Protocol-relative URL //evil.com must NOT be followed
        response = self.client.post(f"{reverse('accounts:login')}?next=//evil.com", {
            'username': self.username,
            'password': self.password,
        })
        self.assertRedirects(response, reverse('store:home'))

    def test_open_redirect_javascript_scheme_blocked(self):
        response = self.client.post(f"{reverse('accounts:login')}?next=javascript:alert(1)", {
            'username': self.username,
            'password': self.password,
        })
        self.assertRedirects(response, reverse('store:home'))

    def test_registration_success(self):
        response = self.client.post(reverse('accounts:register'), {
            'first_name': 'New',
            'last_name': 'Person',
            'username': 'newperson',
            'email': 'new@example.com',
            'password1': 'NewPassWord123!',
            'password2': 'NewPassWord123!',
        })
        self.assertRedirects(response, reverse('store:home'))
        self.assertTrue(User.objects.filter(username='newperson').exists())

    def test_registration_duplicate_email_rejected(self):
        response = self.client.post(reverse('accounts:register'), {
            'first_name': 'New',
            'last_name': 'Person',
            'username': 'differentuser',
            'email': 'testuser@example.com',  # duplicate email
            'password1': 'NewPassWord123!',
            'password2': 'NewPassWord123!',
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "An account with this email already exists.")

    def test_logout_post(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.post(reverse('accounts:logout'))
        self.assertRedirects(response, reverse('store:home'))

    def test_profile_unauthenticated_redirects_to_login(self):
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.url.startswith(reverse('accounts:login')))

    def test_profile_authenticated_access_and_update(self):
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Account Information")

        # Update profile
        update_response = self.client.post(reverse('accounts:profile'), {
            'first_name': 'UpdatedName',
            'last_name': 'User',
            'email': 'updated@example.com',
        })
        self.assertRedirects(update_response, reverse('accounts:profile'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'UpdatedName')
