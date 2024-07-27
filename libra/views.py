from django.contrib.auth.models import AnonymousUser
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import ListView, TemplateView

from .mixins import ReaderRequiredMixin, LibRequiredMixin
from .models import Book, MyBook
from users.models import Reader
from .forms import BorrowBookForm, ReturnBookForm


class BaseViews(TemplateView):
    template_name = 'libra/base.html'


class BookListView(ReaderRequiredMixin, View):
    template_name = 'libra/home.html'

    def get(self, request):
        if isinstance(request.user, AnonymousUser):
            return render(request, self.template_name, {'error': 'Пользователь не авторизован.'})

        try:
            reader = Reader.objects.get(user=request.user)
        except Reader.DoesNotExist:
            return render(request, self.template_name, {'error': 'Пользователь не зарегистрирован как читатель.'})

        books = Book.objects.all()
        books_with_status = []
        for book in books:
            mybook = book.mybook_set.filter(reader=reader, return_date__isnull=True).first()
            is_borrowed = mybook is not None
            borrow_form = None if is_borrowed else BorrowBookForm(initial={'book_id': book.id})
            return_form = ReturnBookForm(initial={'mybook_id': mybook.id}) if is_borrowed else None
            books_with_status.append((book, is_borrowed, borrow_form, return_form))
        return render(request, self.template_name, {'books_with_status': books_with_status})

    def post(self, request):
        if isinstance(request.user, AnonymousUser):
            return render(request, self.template_name, {'error': 'Пользователь не авторизован.'})

        try:
            reader = Reader.objects.get(user=request.user)
        except Reader.DoesNotExist:
            return render(request, self.template_name, {'error': 'Пользователь не зарегистрирован как читатель.'})

        if 'borrow' in request.POST:
            form = BorrowBookForm(request.POST)
            if form.is_valid():
                book_id = form.cleaned_data['book_id']
                book = get_object_or_404(Book, id=book_id)
                MyBook.objects.create(book=book, reader=reader)
        elif 'return' in request.POST:
            form = ReturnBookForm(request.POST)
            if form.is_valid():
                mybook_id = form.cleaned_data['mybook_id']
                mybook = get_object_or_404(MyBook, id=mybook_id)
                if mybook.reader == reader:
                    mybook.return_date = timezone.now()
                    mybook.save()
        return redirect('book_list')


class MyBooksView(ReaderRequiredMixin, ListView):
    model = MyBook
    template_name = 'libra/my_books.html'
    context_object_name = 'my_books'

    def get_queryset(self):
        reader = Reader.objects.get(user=self.request.user)
        return MyBook.objects.filter(
            reader=reader,
            return_date__isnull=True
        ).order_by('book__title')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for book in context['my_books']:
            book.days_borrowed = (timezone.now() - book.borrow_date).days
        return context


class DebtorsListView(LibRequiredMixin, View):
    template_name = 'libra/debtors_list.html'

    def get(self, request):
        overdue_books = MyBook.objects.filter(return_date__isnull=True).select_related('reader', 'book')

        debtors_list = []
        for mybook in overdue_books:
            days_borrowed = (timezone.now().date() - mybook.borrow_date.date()).days
            debtors_list.append({
                'username': mybook.reader.user.username,
                'first_name': mybook.reader.user.first_name,
                'last_name': mybook.reader.user.last_name,
                'address': mybook.reader.address,
                'book_title': mybook.book.title,
                'borrow_date': mybook.borrow_date,
                'days_borrowed': days_borrowed
            })

        return render(request, self.template_name, {'debtors_list': debtors_list})
