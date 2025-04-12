from django.db import models

# Create your models here.


class GuidanceAuthority(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    university_name = models.CharField(max_length=255)
    sent_deadline = models.DateField()
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    backup_email = models.EmailField(
        unique=True, null=True, blank=True)

    def __str__(self):
        return self.name


INTERFACE_ROLES = (
    ('cati', 'CATI'),
    ('cde', 'CDE'),
    ('bi', 'Business Incubator'),
)


class Interfaces(models.Model):
    interface_role = models.CharField(
        max_length=4,
        choices=INTERFACE_ROLES,
        default='cati',
    )
    university_name = models.CharField(max_length=255)
    guidance_authority = models.ForeignKey(
        GuidanceAuthority, on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    backup_email = models.EmailField(
        unique=True, null=True, blank=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.interface_role} - {self.university_name}"
