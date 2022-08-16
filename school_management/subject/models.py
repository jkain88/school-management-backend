from django.db import models
from model_utils.models import TimeStampedModel

from school_management.core import GradeLevel


class Subject(models.Model):
    name = models.CharField(max_length=200, blank=False)
    schedule = models.DateTimeField()
    course = models.CharField(max_length=100, blank=True)
    grade_level = models.CharField(choices=GradeLevel.CHOICES, max_length=50, blank=True)


class Grade(TimeStampedModel):
    subject = models.OneToOneField(Subject, on_delete=models.PROTECT)
    value = models.DecimalField(max_digits=5, decimal_places=2)
