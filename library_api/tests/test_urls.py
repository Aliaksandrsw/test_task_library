from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from libra.models import Reader, Book, MyBook

User = get_user_model()


class URLTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.reader_user = User.objects.create_user(username='readeruser', password='readerpass123')
        self.reader = Reader.objects.create(user=self.reader_user)
        self.book = Book.objects.create(title='Test Book', author='Test Author')

    def test_books_list_url(self):
        self.client.force_authenticate(user=self.reader_user)
        response = self.client.get(reverse('book-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mybooks_list_url_for_reader(self):
        self.client.force_authenticate(user=self.reader_user)
        response = self.client.get(reverse('mybook-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mybooks_list_url_for_non_reader(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.get(reverse('mybook-list'))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_borrow_book(self):
        self.client.force_authenticate(user=self.reader_user)
        response = self.client.post(reverse('book-borrow', kwargs={'pk': self.book.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_return_book(self):
        self.client.force_authenticate(user=self.reader_user)
        MyBook.objects.create(book=self.book, reader=self.reader)
        response = self.client.post(reverse('book-return-book', kwargs={'pk': self.book.pk}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_obtain_url(self):
        response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'readeruser',
            'password': 'readerpass123'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_token_refresh_url(self):
        obtain_response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'readeruser',
            'password': 'readerpass123'
        })
        refresh_token = obtain_response.data['refresh']
        response = self.client.post(reverse('token_refresh'), {'refresh': refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_token_verify_url(self):
        obtain_response = self.client.post(reverse('token_obtain_pair'), {
            'username': 'readeruser',
            'password': 'readerpass123'
        })
        access_token = obtain_response.data['access']
        response = self.client.post(reverse('token_verify'), {'token': access_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
