from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from libra.models import Book, MyBook


@admin.register(Book)
class BookkAdmin(SimpleHistoryAdmin):
    list_display = ['title','author','genre']

class UnreturnedBooksFilter(admin.SimpleListFilter):
    title = 'Невозвращенные книги'
    parameter_name = 'unreturned'

    def lookups(self, request, model_admin):
        return (
            ('+', 'Невозврат'),
        )

    def queryset(self, request, queryset):
        if self.value() == '+':
            return queryset.filter(return_date__isnull=True)
        return queryset


@admin.register(MyBook)
class MyBookAdmin(SimpleHistoryAdmin):
    fields = ['book', 'reader', 'borrow_date', 'return_date']
    readonly_fields = ['borrow_date']
    list_display = ['book', 'reader', 'borrow_date', 'return_date']
    list_filter = [UnreturnedBooksFilter]
