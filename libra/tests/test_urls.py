from django.test import TestCase
from django.urls import reverse


class TestUrls(TestCase):

    def test_start_url(self):
        url = reverse('start')
        self.assertEqual(url, '/')

    def test_book_list_url(self):
        url = reverse('book_list')
        self.assertEqual(url, '/reader/')

    def test_my_books_url(self):
        url = reverse('my_books')
        self.assertEqual(url, '/reader/my-books/')

    def test_debtors_list_url(self):
        url = reverse('debtors_list')
        self.assertEqual(url, '/libra/debtors/')