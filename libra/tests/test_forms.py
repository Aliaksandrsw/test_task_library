from django.test import TestCase
from libra.forms import BorrowBookForm, ReturnBookForm


class TestForms(TestCase):

    def test_borrow_book_form_field(self):
        form = BorrowBookForm()
        self.assertTrue('book_id' in form.fields)
        self.assertEqual(form.fields['book_id'].label, None)
        self.assertEqual(form.fields['book_id'].widget.input_type, 'hidden')

    def test_return_book_form_field(self):
        form = ReturnBookForm()
        self.assertTrue('mybook_id' in form.fields)
        self.assertEqual(form.fields['mybook_id'].label, None)
        self.assertEqual(form.fields['mybook_id'].widget.input_type, 'hidden')
