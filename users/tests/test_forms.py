from django.test import TestCase
from django.contrib.auth import get_user_model
from users.forms import LoginUserForm, RegisterUserFormReader, RegisterUserFormLibrian
from users.models import Reader, Librarian

User = get_user_model()


class LoginUserFormTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword123'
        )

    def test_login_form_valid_data(self):
        form = LoginUserForm(data={
            'username': 'testuser',
            'password': 'testpassword123'
        })
        self.assertTrue(form.is_valid())

    def test_login_form_no_data(self):
        form = LoginUserForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 2)


class RegisterUserFormReaderTest(TestCase):
    def test_register_reader_form_valid_data(self):
        form = RegisterUserFormReader(data={
            'username': 'newreader',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'first_name': 'John',
            'last_name': 'Doe',
            'address': '123 Test St, Test City'
        })
        self.assertTrue(form.is_valid())

    def test_register_reader_form_passwords_dont_match(self):
        form = RegisterUserFormReader(data={
            'username': 'newreader',
            'password1': 'testpassword123',
            'password2': 'differentpassword',
            'first_name': 'John',
            'last_name': 'Doe',
            'address': '123 Test St, Test City'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_register_reader_form_missing_fields(self):
        form = RegisterUserFormReader(data={
            'username': 'newreader',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors)
        self.assertIn('last_name', form.errors)
        self.assertIn('address', form.errors)

    def test_register_reader_form_save(self):
        form = RegisterUserFormReader(data={
            'username': 'newreader',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'first_name': 'John',
            'last_name': 'Doe',
            'address': '123 Test St, Test City'
        })
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.role, 'RDR')
        self.assertTrue(Reader.objects.filter(user=user).exists())
        reader = Reader.objects.get(user=user)
        self.assertEqual(reader.first_name, 'John')
        self.assertEqual(reader.last_name, 'Doe')
        self.assertEqual(reader.address, '123 Test St, Test City')


class RegisterUserFormLibrianTest(TestCase):
    def test_register_librarian_form_valid_data(self):
        form = RegisterUserFormLibrian(data={
            'username': 'newlibrarian',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        })
        self.assertTrue(form.is_valid())

    def test_register_librarian_form_passwords_dont_match(self):
        form = RegisterUserFormLibrian(data={
            'username': 'newlibrarian',
            'password1': 'testpassword123',
            'password2': 'differentpassword'
        })
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_register_librarian_form_save(self):
        form = RegisterUserFormLibrian(data={
            'username': 'newlibrarian',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        })
        self.assertTrue(form.is_valid())
        user = form.save()
        self.assertEqual(user.role, 'LIB')
        self.assertTrue(Librarian.objects.filter(user=user).exists())
