# Generated by Django 5.2 on 2025-04-12 11:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("projects", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="project",
            name="is_complete",
            field=models.BooleanField(default=False),
        ),
    ]
