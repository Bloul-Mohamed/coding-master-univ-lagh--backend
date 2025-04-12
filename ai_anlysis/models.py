from django.db import models
from projects.models import Project


class ProjectAnalysis(models.Model):
    project = models.OneToOneField(
        Project,
        on_delete=models.CASCADE,
        related_name='ai_analysis'
    )
    improved_description = models.TextField(blank=True, null=True)
    idea_score = models.FloatField(default=0.0)  # Score from 0 to 10
    suggestions = models.TextField(blank=True, null=True)
    admin_approved = models.BooleanField(default=False)
    analysis_date = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Analysis for {self.project.title}"
