from django.contrib.auth import get_user_model
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from libra.models import Book, MyBook, Reader
from django.utils import timezone

User = get_user_model()


class BookViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.reader = Reader.objects.create(user=self.user)
        self.book = Book.objects.create(title='Test Book', author='Test Author')
        self.client.force_authenticate(user=self.user)

    def test_list_books(self):
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_borrow_book(self):
        response = self.client.post(f'/api/books/{self.book.id}/borrow/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Книга взята.')

    def test_borrow_book_twice(self):
        self.client.post(f'/api/books/{self.book.id}/borrow/')
        response = self.client.post(f'/api/books/{self.book.id}/borrow/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'У вас уже есть эта книга.')

    def test_return_book(self):
        MyBook.objects.create(book=self.book, reader=self.reader)
        response = self.client.post(f'/api/books/{self.book.id}/return_book/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['detail'], 'Книга возвращена.')

    def test_return_book_not_borrowed(self):
        response = self.client.post(f'/api/books/{self.book.id}/return_book/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['detail'], 'У вас нет этой книги.')


class MyBookViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.reader = Reader.objects.create(user=self.user)
        self.book = Book.objects.create(title='Test Book', author='Test Author')
        self.my_book = MyBook.objects.create(book=self.book, reader=self.reader)
        self.client.force_authenticate(user=self.user)

    def test_list_my_books(self):
        response = self.client.get('/api/mybooks/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_list_my_books_non_reader(self):
        non_reader_user = User.objects.create_user(username='nonreader', password='12345')
        self.client.force_authenticate(user=non_reader_user)
        response = self.client.get('/api/mybooks/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], 'User is not a reader.')
