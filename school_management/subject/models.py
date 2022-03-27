from django.db import models

from ..core import GradeLevel


class Subject(models.Model):
    name = models.CharField(max_length=200, blank=False)
    schedule = models.DateTimeField()
    course = models.CharField(max_length=100, blank=True)
    grade_level = models.CharField(choices=GradeLevel.CHOICES, max_length=50, blank=True)
