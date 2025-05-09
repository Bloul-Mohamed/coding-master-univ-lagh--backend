# Generated by Django 5.2 on 2025-04-12 09:58

import django.db.models.deletion
import django_countries.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Project",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("send_date", models.DateField(auto_now_add=True)),
                ("update_date", models.DateField(auto_now=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("S", "sent"),
                            ("P", "In progress"),
                            ("CDE", "Directed to  CDE"),
                            ("CATI", "Directed to  CATI"),
                            ("bi", "Directed to Business Incubator"),
                            ("I", "Inadmissible"),
                            ("N", "None"),
                        ],
                        default="N",
                        max_length=100,
                    ),
                ),
                ("deadline", models.BooleanField(default=True)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("password", models.CharField(max_length=255)),
                (
                    "backup_email",
                    models.EmailField(
                        blank=True, max_length=254, null=True, unique=True
                    ),
                ),
                (
                    "guidance_authority",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="accounts.guidanceauthority",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Student",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("first_name", models.CharField(max_length=255)),
                ("last_name", models.CharField(max_length=255)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("phone_number", models.CharField(max_length=15)),
                ("university_name", models.CharField(max_length=255)),
                ("country", django_countries.fields.CountryField(max_length=2)),
                (
                    "project",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="students",
                        to="projects.project",
                    ),
                ),
            ],
        ),
    ]
