from django.test import TestCase
from django.contrib.auth import get_user_model
from libra.models import *
from users.models import *

User = get_user_model()


class BookModelTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Тестовая книга",
            author="Тестовый автор",
            genre="Тестовый жанр"
        )

    def test_book_creation(self):
        self.assertEqual(self.book.title, "Тестовая книга")
        self.assertEqual(self.book.author, "Тестовый автор")
        self.assertEqual(self.book.genre, "Тестовый жанр")

    def test_book_str_method(self):
        self.assertEqual(str(self.book), "Тестовая книга")


class MyBookModelTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Тестовая книга",
            author="Тестовый автор",
            genre="Тестовый жанр"
        )
        self.user = User.objects.create_user(
            username="testuser",
            password="testpass123",
            role="RDR"
        )
        self.reader = Reader.objects.create(
            user=self.user,
            first_name="Тест",
            last_name="Читатель",
            address="Тестовый адрес"
        )
        self.my_book = MyBook.objects.create(
            book=self.book,
            reader=self.reader
        )

    def test_mybook_creation(self):
        self.assertEqual(self.my_book.book, self.book)
        self.assertEqual(self.my_book.reader, self.reader)
        self.assertIsNotNone(self.my_book.borrow_date)
        self.assertIsNone(self.my_book.return_date)

    def test_mybook_str_method(self):
        self.assertEqual(str(self.my_book), "Тестовая книга")

    def test_mybook_return(self):
        from django.utils import timezone
        self.my_book.return_date = timezone.now()
        self.my_book.save()
        self.assertIsNotNone(self.my_book.return_date)
