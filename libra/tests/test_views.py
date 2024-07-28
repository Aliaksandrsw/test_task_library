from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from libra.models import Book, MyBook
from users.models import Reader, Librarian

User = get_user_model()


class BaseViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.start_url = reverse('start')

    def test_base_view(self):
        response = self.client.get(self.start_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'libra/base.html')


class BookListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.book_list_url = reverse('book_list')
        self.login_url = reverse('users:login')
        self.user = User.objects.create_user(username='testuser', password='12345', role='RDR')
        self.reader = Reader.objects.create(user=self.user, first_name='Test', last_name='User', address='Test Address')
        self.book = Book.objects.create(title='Test Book', author='Test Author', genre='Test Genre')

    def test_book_list_view_authenticated(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.book_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'libra/home.html')
        self.assertIn('books_with_status', response.context)

    def test_book_list_view_unauthenticated(self):
        response = self.client.get(self.book_list_url)
        expected_redirect_url = f'{self.login_url}?next={self.book_list_url}'
        self.assertRedirects(response, expected_redirect_url, fetch_redirect_response=False)

    def test_borrow_book(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(self.book_list_url, {'borrow': 'Borrow', 'book_id': self.book.id})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(MyBook.objects.filter(book=self.book, reader=self.reader).exists())

    def test_return_book(self):
        self.client.login(username='testuser', password='12345')
        mybook = MyBook.objects.create(book=self.book, reader=self.reader)
        response = self.client.post(self.book_list_url, {'return': 'Return', 'mybook_id': mybook.id})
        self.assertEqual(response.status_code, 302)
        mybook.refresh_from_db()
        self.assertIsNotNone(mybook.return_date)


class MyBooksViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.my_books_url = reverse('my_books')
        self.user = User.objects.create_user(username='testuser', password='12345', role='RDR')
        self.reader = Reader.objects.create(user=self.user, first_name='Test', last_name='User', address='Test Address')
        self.book = Book.objects.create(title='Test Book', author='Test Author', genre='Test Genre')
        self.mybook = MyBook.objects.create(book=self.book, reader=self.reader)

    def test_my_books_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(self.my_books_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'libra/my_books.html')
        self.assertIn('my_books', response.context)
        self.assertEqual(len(response.context['my_books']), 1)


class DebtorsListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.debtors_list_url = reverse('debtors_list')
        self.lib_user = User.objects.create_user(username='libuser', password='12345', role='LIB')
        self.librarian = Librarian.objects.create(user=self.lib_user)
        self.reader_user = User.objects.create_user(username='readeruser', password='12345', role='RDR')
        self.reader = Reader.objects.create(user=self.reader_user, first_name='Test', last_name='Reader',
                                            address='Test Address')
        self.book = Book.objects.create(title='Test Book', author='Test Author', genre='Test Genre')
        self.mybook = MyBook.objects.create(book=self.book, reader=self.reader,
                                            borrow_date=timezone.now() - timezone.timedelta(days=30))

    def test_debtors_list_view(self):
        self.client.login(username='libuser', password='12345')
        response = self.client.get(self.debtors_list_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'libra/debtors_list.html')
        self.assertIn('debtors_list', response.context)
        self.assertEqual(len(response.context['debtors_list']), 1)
        self.assertEqual(response.context['debtors_list'][0]['username'], 'readeruser')
