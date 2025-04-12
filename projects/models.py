# Fix for projects/models.py

from django.db import models
from django_countries.fields import CountryField
from accounts.models import GuidanceAuthority

# Create your models here.
STAUTS = (
    ('S', 'sent'),
    ('P', 'In progress'),
    ('CDE', 'Directed to  CDE'),
    ('CATI', 'Directed to  CATI'),
    ('bi', 'Directed to Business Incubator'),
    ('I', 'Inadmissible'),
    ('N', 'None'),
)


class Project(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    send_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)
    status = models.CharField(
        max_length=100,
        choices=STAUTS,
        default='N',
    )
    guidance_authority = models.ForeignKey(
        GuidanceAuthority, on_delete=models.CASCADE)
    deadline = models.BooleanField(default=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    backup_email = models.EmailField(
        unique=True, null=True, blank=True)
    is_complete = models.BooleanField(default=False)  # New field added

    def __str__(self):
        return self.title


class Student(models.Model):
    id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    project = models.ForeignKey(
        Project, on_delete=models.CASCADE, related_name='students')
    university_name = models.CharField(max_length=255)
    country = CountryField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
