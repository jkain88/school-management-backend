from django.contrib.auth.models import AbstractBaseUser
from django.db import models

from . import Role


class Address(models.Model):
    street = models.CharField(max_length=100, blank=True),
    city_area = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=70, blank=True)
    province = models.CharField(max_length=70, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)


class User(AbstractBaseUser):
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    age = models.PositiveIntegerField()
    role = models.CharField(max_length=20, blank=True, choices=Role.CHOICES)
