from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from . import Role, AddressType


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    role = models.CharField(max_length=20, choices=Role.CHOICES)
    contact_number = PhoneNumberField(blank=True)
    objects = UserManager()

    USERNAME_FIELD = "email"


class Address(models.Model):
    street = models.CharField(max_length=100, blank=True)
    city_area = models.CharField(max_length=100)
    city = models.CharField(max_length=70)
    province = models.CharField(max_length=70)
    postal_code = models.CharField(max_length=20)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="addresses")
    address_type = models.CharField(max_length=15, choices=AddressType.CHOICES)

