from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from users.forms import *

User = get_user_model()


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация'
        return context

    def get_success_url(self):
        user = self.request.user
        if user.role == 'LIB':
            return reverse_lazy('debtors_list')
        else:
            return reverse_lazy('book_list')


class RegisterReader(CreateView):
    form_class = RegisterUserFormReader
    template_name = 'users/register.html'
    extra_context = {
        'title': "Регистрация",
    }
    success_url = reverse_lazy('users:login')


class RegisterLibrian(CreateView):
    form_class = RegisterUserFormLibrian
    template_name = 'users/register.html'
    extra_context = {
        'title': "Регистрация",
    }
    success_url = reverse_lazy('users:login')
