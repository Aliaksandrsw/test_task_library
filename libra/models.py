from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from users.models import Reader


class Book(models.Model):
    title = models.CharField(max_length=200, verbose_name='Название')
    author = models.CharField(max_length=100, verbose_name='Автор')
    genre = models.CharField(max_length=50, verbose_name='Жанр')
    history = HistoricalRecords()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class MyBook(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')
    reader = models.ForeignKey(Reader, on_delete=models.CASCADE, verbose_name='Читатель')
    borrow_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата взятия')
    return_date = models.DateTimeField(null=True, blank=True, verbose_name='Дата возврата')
    history = HistoricalRecords()

    def __str__(self):
        return self.book.title
