from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .models import Project, Student
from .serializers import ProjectSerializer, StudentSerializer, ProjectStatusUpdateSerializer
from accounts.models import GuidanceAuthority, Interfaces


class ProjectViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Project management
    """
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend,
                       filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'guidance_authority',
                        'deadline', 'is_complete']
    search_fields = ['title', 'description']
    ordering_fields = ['send_date', 'update_date',
                       'title']

    @action(detail=True, methods=['post'])
    def update_status(self, request, pk=None):
        """
        Update the status of a project
        """
        project = self.get_object()
        serializer = ProjectStatusUpdateSerializer(data=request.data)

        if serializer.is_valid():
            project.status = serializer.validated_data['status']
            project.save()
            return Response({'status': 'project status updated'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def toggle_completion(self, request, pk=None):
        """
        Toggle the completion status of a project
        """
        project = self.get_object()
        project.is_complete = not project.is_complete
        project.save()
        return Response({
            'status': 'success',
            'is_complete': project.is_complete,
            'message': f'Project marked as {"complete" if project.is_complete else "incomplete"}'
        })

    @action(detail=False, methods=['get'])
    def completed(self, request):
        """
        Get all completed projects
        """
        projects = Project.objects.filter(is_complete=True)
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def incomplete(self, request):
        """
        Get all incomplete projects
        """
        projects = Project.objects.filter(is_complete=False)
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_guidance_authority(self, request):
        """
        Get projects for a specific guidance authority
        """
        authority_id = request.query_params.get('authority_id')
        if not authority_id:
            return Response({'error': 'authority_id parameter is required'},
                            status=status.HTTP_400_BAD_REQUEST)

        projects = Project.objects.filter(guidance_authority_id=authority_id)
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def by_interface(self, request):
        """
        Get projects directed to a specific interface
        """
        interface_role = request.query_params.get('role')
        if not interface_role:
            return Response({'error': 'role parameter is required'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Map interface roles to project statuses
        role_to_status = {
            'cati': 'CATI',
            'cde': 'CDE',
            'bi': 'bi'
        }

        if interface_role not in role_to_status:
            return Response({'error': 'Invalid interface role'},
                            status=status.HTTP_400_BAD_REQUEST)

        projects = Project.objects.filter(
            status=role_to_status[interface_role])
        serializer = self.get_serializer(projects, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def export(self, request):
        """
        Endpoint for exporting projects data (placeholder)
        """
        # This would be implemented with actual export functionality
        # For now, just returning a success message
        return Response({
            'message': 'Projects export functionality would be implemented here',
            'format': request.query_params.get('format', 'csv')
        })


class StudentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Student management
    """
    queryset = Student.objects.all()
    serializer_class = StudentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['project', 'university_name',
                        'country', 'field_of_study', 'branch']
    search_fields = ['first_name', 'last_name',
                     'email', 'field_of_study', 'branch']

    def create(self, request, *args, **kwargs):
        """
        Create a new student with manual ID support
        """
        data = request.data.copy()
        student_id = data.pop('id', None)  # Extract ID if provided

        # Check if ID already exists
        if student_id is not None:
            if Student.objects.filter(id=student_id).exists():
                return Response(
                    {'error': f'Student with ID {student_id} already exists'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        # Validate other fields using serializer
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data

        # Create student using the custom manager
        try:
            student = Student.objects.create_with_id(
                student_id=student_id,
                **validated_data
            )
            # Return the created student
            result_serializer = self.get_serializer(student)
            headers = self.get_success_headers(result_serializer.data)
            return Response(
                result_serializer.data,
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['get'])
    def by_project(self, request):
        """
        Get all students for a specific project
        """
        project_id = request.query_params.get('project_id')
        if not project_id:
            return Response({'error': 'project_id parameter is required'},
                            status=status.HTTP_400_BAD_REQUEST)

        students = Student.objects.filter(project_id=project_id)
        serializer = self.get_serializer(students, many=True)
        return Response(serializer.data)
