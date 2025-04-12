from rest_framework import serializers
from .models import ProjectAnalysis


class ProjectAnalysisSerializer(serializers.ModelSerializer):
    """Serializer for ProjectAnalysis model"""

    class Meta:
        model = ProjectAnalysis
        fields = [
            'id', 'project', 'improved_description', 'idea_score',
            'suggestions', 'admin_approved', 'analysis_date', 'last_updated'
        ]
        read_only_fields = ['analysis_date', 'last_updated']


class AnalysisRequestSerializer(serializers.Serializer):
    """Serializer for analysis request"""
    project_id = serializers.IntegerField(required=True)


class AnalysisApprovalSerializer(serializers.Serializer):
    """Serializer for approving analysis"""
    approved = serializers.BooleanField(required=True)


class AnalysisResponseSerializer(serializers.Serializer):
    """Serializer for detailed analysis response"""
    improved_description = serializers.CharField(
        allow_blank=True, allow_null=True)
    idea_score = serializers.FloatField()
    score_details = serializers.JSONField(required=False)
    suggestions = serializers.JSONField(required=False)
    admin_approved = serializers.BooleanField()
