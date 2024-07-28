from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from users.models import Reader, Librarian

User = get_user_model()


class LoginUserTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_url = reverse('users:login')
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_login_view_get(self):
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/login.html')
        self.assertEqual(response.context['title'], 'Авторизация')

    def test_login_view_post_librarian(self):
        self.user.role = 'LIB'
        self.user.save()
        Librarian.objects.create(user=self.user)
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': '12345'})
        self.assertRedirects(response, reverse('debtors_list'))

    def test_login_view_post_reader(self):
        self.user.role = 'READER'
        self.user.save()
        Reader.objects.create(user=self.user, first_name='Test', last_name='User', address='Test Address')
        response = self.client.post(self.login_url, {'username': 'testuser', 'password': '12345'})

        # Проверяем, что пользователь действительно вошел в систему
        self.assertTrue(response.wsgi_request.user.is_authenticated)
        self.assertEqual(response.wsgi_request.user.role, 'READER')

        # Проверяем редирект
        self.assertRedirects(response, reverse('book_list'))

        # Проверяем доступ к странице book_list
        book_list_response = self.client.get(reverse('book_list'))
        self.assertEqual(book_list_response.status_code, 200)


class RegisterReaderTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('users:register_reader')

    def test_register_reader_view_post(self):
        data = {
            'username': 'newreader',
            'password1': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'Иван',
            'last_name': 'Иванов',
            'address': 'ул. Пушкина, д. Колотушкина'
        }
        response = self.client.post(self.register_url, data)
        self.assertRedirects(response, reverse('users:login'))

        # Проверяем, что пользователь и Reader созданы
        self.assertTrue(User.objects.filter(username='newreader').exists())
        user = User.objects.get(username='newreader')
        self.assertTrue(Reader.objects.filter(user=user).exists())

        # Пробуем войти и получить доступ к book_list
        self.client.login(username='newreader', password='testpass123')
        book_list_response = self.client.get(reverse('book_list'))
        self.assertEqual(book_list_response.status_code, 200)


class RegisterLibrarianTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('users:register_lib')

    def test_register_librarian_view_post(self):
        data = {
            'username': 'newlibrarian',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        response = self.client.post(self.register_url, data)
        self.assertRedirects(response, reverse('users:login'))

        # Проверяем, что пользователь и Librarian созданы
        self.assertTrue(User.objects.filter(username='newlibrarian').exists())
        user = User.objects.get(username='newlibrarian')
        self.assertTrue(Librarian.objects.filter(user=user).exists())

        # Пробуем войти и получить доступ к debtors_list
        self.client.login(username='newlibrarian', password='testpass123')
        debtors_list_response = self.client.get(reverse('debtors_list'))
        self.assertEqual(debtors_list_response.status_code, 200)