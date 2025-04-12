from django.db import models
from django.contrib.auth.models import User


class EmailRecord(models.Model):
    """Model to track emails sent to users"""
    subject = models.CharField(max_length=255)
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='received_emails')
    sent_at = models.DateTimeField(auto_now_add=True)
    was_successful = models.BooleanField(default=False)

    def __str__(self):
        return f"Email to {self.recipient.email}: {self.subject}"
