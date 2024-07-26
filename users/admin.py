from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Librarian, Reader


class LibrarianInline(admin.StackedInline):
    model = Librarian
    can_delete = False
    verbose_name_plural = 'Библиотекарь'


class ReaderInline(admin.StackedInline):
    model = Reader
    can_delete = False
    verbose_name_plural = 'Читатель'
    exclude = ('first_name', 'last_name')


class CustomUserAdmin(UserAdmin):
    inlines = (LibrarianInline, ReaderInline)
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser')
    fieldsets = UserAdmin.fieldsets + (
        ('Дополнительная информация', {'fields': ('role',)}),
    )


admin.site.register(User, CustomUserAdmin)
