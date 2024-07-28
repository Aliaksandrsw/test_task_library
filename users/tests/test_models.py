from django.test import TestCase
from users.models import User, Librarian, Reader


class UserModelTests(TestCase):
    def test_create_librarian(self):
        user = User.objects.create(username='librarian1', role='LIB')
        librarian = Librarian.objects.create(user=user, job_number='12345678')

        self.assertEqual(user.username, 'librarian1')
        self.assertEqual(librarian.job_number, '12345678')

    def test_create_reader(self):
        user = User.objects.create(username='reader1', role='RDR')
        reader = Reader.objects.create(user=user, first_name='John', last_name='Doe', address='123 Main St')

        self.assertEqual(user.username, 'reader1')
        self.assertEqual(reader.first_name, 'John')
        self.assertEqual(reader.last_name, 'Doe')
        self.assertEqual(reader.address, '123 Main St')