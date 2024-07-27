from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django import forms
from .models import Reader, Librarian

User = get_user_model()


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин",
                               widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label="Пароль",
                               widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ['username', 'password']


class RegisterUserFormReader(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-input'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-input'}),
        }

    first_name = forms.CharField(label='Имя', max_length=100, widget=forms.TextInput(attrs={'class': 'form-input'}))
    last_name = forms.CharField(label='Фамилия ', max_length=100, widget=forms.TextInput(attrs={'class': 'form-input'}))
    address = forms.CharField(label='Адрес', widget=forms.Textarea(attrs={'class': 'form-input'}))

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'RDR'
        if commit:
            user.save()
            Reader.objects.create(
                user=user,
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                address=self.cleaned_data['address']
            )
        return user


class RegisterUserFormLibrian(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-input'}),
            'password1': forms.TextInput(attrs={'class': 'form-input'}),

        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'LIB'
        if commit:
            user.save()
            Librarian.objects.create(
                user=user
            )
        return user
