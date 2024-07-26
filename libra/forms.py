from django import forms
from .models import Book, MyBook


class BorrowBookForm(forms.Form):
    book_id = forms.IntegerField(widget=forms.HiddenInput())


class ReturnBookForm(forms.Form):
    mybook_id = forms.IntegerField(widget=forms.HiddenInput())
