from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from users.models import Reader, Librarian


class ReaderRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and Reader.objects.filter(user=self.request.user).exists()


class LibRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and Librarian.objects.filter(user=self.request.user).exists()