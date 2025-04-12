
from rest_framework import status, views
from rest_framework.response import Response
from accounts.models import GuidanceAuthority, Interfaces
from projects.models import Project
from django.shortcuts import get_object_or_404


class LoginView(views.APIView):
    """
    API endpoint for users to log in
    """
    permission_classes = []  # Allow unauthenticated access

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        # Default to project login
        user_type = request.data.get('user_type', 'project')

        if not email or not password:
            return Response({'error': 'Email and password are required'},
                            status=status.HTTP_400_BAD_REQUEST)

        if user_type == 'guidance_authority':
            try:
                user = GuidanceAuthority.objects.get(email=email)
                if user.password == password:  # In a real app, use proper password verification
                    return Response({
                        'id': user.id,
                        'name': user.name,
                        'user_type': 'guidance_authority',
                        'message': 'Login successful'
                    })
            except GuidanceAuthority.DoesNotExist:
                pass

        elif user_type == 'interface':
            try:
                user = Interfaces.objects.get(email=email)
                if user.password == password:  # In a real app, use proper password verification
                    return Response({
                        'id': user.id,
                        'interface_role': user.interface_role,
                        'user_type': 'interface',
                        'message': 'Login successful'
                    })
            except Interfaces.DoesNotExist:
                pass

        elif user_type == 'project':
            try:
                user = Project.objects.get(email=email)
                if user.password == password:  # In a real app, use proper password verification
                    return Response({
                        'id': user.id,
                        'title': user.title,
                        'user_type': 'project',
                        'message': 'Login successful'
                    })
            except Project.DoesNotExist:
                pass

        return Response({'error': 'Invalid credentials'},
                        status=status.HTTP_401_UNAUTHORIZED)
