import json
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from asgiref.sync import sync_to_async

from projects.models import Project
from .models import ProjectAnalysis
from .serializers import (
    ProjectAnalysisSerializer,
    AnalysisRequestSerializer,
    AnalysisApprovalSerializer,
    AnalysisResponseSerializer
)
from .gemini_client import GeminiClient


class ProjectAnalysisViewSet(viewsets.ModelViewSet):
    """ViewSet for Project Analysis"""
    queryset = ProjectAnalysis.objects.all()
    serializer_class = ProjectAnalysisSerializer

    def get_permissions(self):
        """
        Custom permissions:
        - Admin approval requires admin permission
        - Other actions use default permissions
        """
        if self.action == 'approve_analysis':
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.IsAuthenticated]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['post'])
    async def analyze_project(self, request):
        """
        Analyze a project using Gemini AI
        """
        serializer = AnalysisRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        project_id = serializer.validated_data['project_id']

        # Get project asynchronously
        project = await sync_to_async(get_object_or_404)(Project, id=project_id)

        # Project data to send to AI
        project_data = {
            'id': project.id,
            'title': project.title,
            'description': project.description,
        }

        # Initialize Gemini client
        client = GeminiClient()

        # Get AI analysis
        improved_description = await client.improve_description(project_data)
        idea_score, score_details = await client.score_idea(project_data)
        suggestions_data = await client.get_suggestions(project_data)

        # Convert suggestions to JSON string for storage
        suggestions_json = json.dumps(suggestions_data)

        # Create or update analysis record
        analysis, created = await sync_to_async(
            ProjectAnalysis.objects.update_or_create
        )(
            project=project,
            defaults={
                'improved_description': improved_description,
                'idea_score': idea_score,
                'suggestions': suggestions_json,
                'admin_approved': False  # Reset approval status on update
            }
        )

        # Format response
        response_data = {
            'improved_description': improved_description,
            'idea_score': idea_score,
            'score_details': score_details,
            'suggestions': suggestions_data,
            'admin_approved': analysis.admin_approved
        }

        response_serializer = AnalysisResponseSerializer(data=response_data)
        if response_serializer.is_valid():
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        return Response(response_serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=True, methods=['post'])
    def approve_analysis(self, request, pk=None):
        """
        Approve or reject an analysis (admin only)
        """
        analysis = self.get_object()
        serializer = AnalysisApprovalSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        analysis.admin_approved = serializer.validated_data['approved']
        analysis.save()

        return Response({
            'id': analysis.id,
            'admin_approved': analysis.admin_approved,
            'message': f"Analysis {'approved' if analysis.admin_approved else 'rejected'} successfully"
        })

    @action(detail=False, methods=['get'])
    def pending_approval(self, request):
        """
        Get all analyses pending admin approval
        """
        pending = ProjectAnalysis.objects.filter(admin_approved=False)
        serializer = self.get_serializer(pending, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def get_by_project(self, request):
        """
        Get analysis for a specific project
        """
        project_id = request.query_params.get('project_id')
        if not project_id:
            return Response({'error': 'project_id parameter is required'},
                            status=status.HTTP_400_BAD_REQUEST)

        analysis = get_object_or_404(ProjectAnalysis, project_id=project_id)
        serializer = self.get_serializer(analysis)

        # Parse the JSON string for suggestions to return as JSON object
        response_data = serializer.data
        if response_data.get('suggestions'):
            try:
                response_data['suggestions'] = json.loads(
                    response_data['suggestions'])
            except json.JSONDecodeError:
                pass  # Keep as string if it's not valid JSON

        return Response(response_data)
