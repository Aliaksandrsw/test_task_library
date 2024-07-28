from django.test import TestCase
from django.urls import reverse


class UserViewsTests(TestCase):
    def test_login_view(self):
        response = self.client.get(reverse('users:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')

    def test_logout_view(self):
        response = self.client.post(reverse('users:logout'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('start'))

    def test_register_reader_view(self):
        response = self.client.get(reverse('users:register_reader'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')

    def test_register_librarian_view(self):
        response = self.client.get(reverse('users:register_lib'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/register.html')
