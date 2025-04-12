from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import GuidanceAuthority, Interfaces
from .serializers import GuidanceAuthoritySerializer, InterfacesSerializer


class GuidanceAuthorityViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Guidance Authority management
    """
    queryset = GuidanceAuthority.objects.all()
    serializer_class = GuidanceAuthoritySerializer

    @action(detail=True, methods=['get'])
    def interfaces(self, request, pk=None):
        """
        Get all interfaces associated with this guidance authority
        """
        authority = self.get_object()
        interfaces = Interfaces.objects.filter(guidance_authority=authority)
        serializer = InterfacesSerializer(interfaces, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def update_deadline(self, request, pk=None):
        """
        Update the sent deadline for projects
        """
        authority = self.get_object()
        new_deadline = request.data.get('sent_deadline')

        if not new_deadline:
            return Response({'error': 'sent_deadline field is required'},
                            status=status.HTTP_400_BAD_REQUEST)

        authority.sent_deadline = new_deadline
        authority.save()
        serializer = self.get_serializer(authority)
        return Response(serializer.data)


class InterfacesViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Interfaces management
    """
    queryset = Interfaces.objects.all()
    serializer_class = InterfacesSerializer

    @action(detail=False, methods=['get'])
    def by_role(self, request):
        """
        Filter interfaces by role
        """
        role = request.query_params.get('role', None)
        if role:
            interfaces = Interfaces.objects.filter(interface_role=role)
            serializer = self.get_serializer(interfaces, many=True)
            return Response(serializer.data)
        return Response({'error': 'Role parameter is required'},
                        status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'])
    def upload_training_program(self, request, pk=None):
        """
        Endpoint for interface to upload training program (placeholder)
        """
        # This is a placeholder for functionality described in your specs
        # You'd normally handle file upload here

        return Response({
            'status': 'success',
            'message': 'Training program uploaded successfully'
        })
