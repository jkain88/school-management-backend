from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from . import (
    Role,
    AddressType,
    Sex
)


class Address(models.Model):
    street = models.CharField(max_length=100, blank=True)
    city_area = models.CharField(max_length=100)
    city = models.CharField(max_length=70)
    province = models.CharField(max_length=70)
    postal_code = models.CharField(max_length=20)
    address_type = models.CharField(max_length=15, choices=AddressType.CHOICES)


class BaseUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    sex = models.CharField(max_length=20, choices=Sex.CHOICES)
    contact_number = PhoneNumberField(blank=True)
    addresses = models.ManyToManyField(Address)
    objects = UserManager()

    USERNAME_FIELD = "email"

    class Meta:
        abstract = True


class Student(BaseUser):
    mother_name = models.CharField(max_length=200, blank=True)
    father_name = models.CharField(max_length=200, blank=True)
