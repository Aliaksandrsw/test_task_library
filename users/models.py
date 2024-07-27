import random

from django.contrib.auth.models import AbstractUser
from django.db import models


def generate_job_number():
    return ''.join(random.choices('0123456789', k=8))


class User(AbstractUser):
    ROLE_CHOICES = [
        ('LIB', 'Библиотекарь'),
        ('RDR', 'Читатель'),
    ]

    role = models.CharField(max_length=3, choices=ROLE_CHOICES, default='RDR')


class Librarian(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    job_number = models.CharField(
        max_length=50,
        unique=True,
        default=generate_job_number(),
        verbose_name='Табельный номер'
    )

    def save(self, *args, **kwargs):
        while not self.pk and Librarian.objects.filter(job_number=self.job_number).exists():
            self.job_number = ''.join(random.choices('0123456789', k=8))
        super().save(*args, **kwargs)


class Reader(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    first_name = models.CharField(max_length=100, verbose_name='Имя')
    last_name = models.CharField(max_length=100, verbose_name='Фамилиия')
    address = models.TextField(verbose_name='Адрес')

    def __str__(self):
        return self.user.username
