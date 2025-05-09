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


class StudentManager(models.Manager):
    def create_with_id(self, student_id=None, **kwargs):
        """
        Create a student with a specific ID if provided
        """
        student = self.model(**kwargs)
        if student_id is not None:
            student.id = student_id
        student.save()
        return student


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
    field_of_study = models.CharField(max_length=255, null=True, blank=True)
    branch = models.CharField(max_length=255, null=True, blank=True)
    objects = StudentManager()  # Use the custom manager
    # Additional fields for user management but is not required
    user_id = models.CharField(max_length=255, null=True, blank=True)
    uuid = models.CharField(max_length=255, null=True, blank=True)
    id_individual = models.CharField(max_length=255, null=True, blank=True)
    establishment_id = models.CharField(max_length=255, null=True, blank=True)
    user_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
