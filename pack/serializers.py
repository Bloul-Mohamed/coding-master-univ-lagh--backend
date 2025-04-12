from rest_framework import serializers


class EmailSerializer(serializers.Serializer):
    """Serializer for sending an email to a single user"""
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField(help_text="HTML content is supported")


class BulkEmailSerializer(serializers.Serializer):
    """Serializer for sending emails to multiple users"""
    subject = serializers.CharField(max_length=255)
    message = serializers.CharField(help_text="HTML content is supported")
    user_ids = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="List of user IDs to send emails to"
    )
