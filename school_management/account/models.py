from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from ..subject.models import Subject
from . import (
    Role,
    AddressType,
    Sex
)


class UserManager(BaseUserManager):
    def create_user(
        self, email, password=None, is_staff=False, **extra_fields
    ):
        """Create a user instance with the given email and password."""
        email = UserManager.normalize_email(email)
        extra_fields.pop("username", None)

        user = self.model(
            email=email, is_staff=is_staff, **extra_fields
        )
        if password:
            user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_user(
            email, password, is_superuser=True, is_staff=False, is_active=True, **extra_fields
        )


class Address(models.Model):
    street = models.CharField(max_length=100, blank=True)
    city_area = models.CharField(max_length=100)
    city = models.CharField(max_length=70)
    province = models.CharField(max_length=70)
    postal_code = models.CharField(max_length=20)
    address_type = models.CharField(max_length=15, choices=AddressType.CHOICES)


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(null=True)
    sex = models.CharField(max_length=20, choices=Sex.CHOICES)
    contact_number = PhoneNumberField(blank=True)
    addresses = models.ManyToManyField(Address)
    role = models.CharField(choices=Role.CHOICES, blank=True, max_length=70)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    objects = UserManager()

    USERNAME_FIELD = "email"


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    mother_name = models.CharField(max_length=200, blank=True)
    father_name = models.CharField(max_length=200, blank=True)
    subjects = models.ManyToManyField(Subject)


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    students = models.ManyToManyField(StudentProfile, related_name="teachers")
    subjects = models.ManyToManyField(Subject)
