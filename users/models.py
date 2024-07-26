from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CHOICES = [
        ('LIB', 'Библиотекарь'),
        ('RDR', 'Читатель'),
    ]

    role = models.CharField(max_length=3, choices=ROLE_CHOICES, default='RDR')


class Librarian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    job_number = models.CharField(max_length=50, unique=True, verbose_name='Табельный номер')


class Reader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилиия')
    address = models.TextField(verbose_name='Адрес')

    def __str__(self):
        return self.user.username
