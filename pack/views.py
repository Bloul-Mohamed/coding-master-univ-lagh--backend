from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.utils.html import strip_tags
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import datetime

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import EmailRecord
from .serializers import EmailSerializer, BulkEmailSerializer

# Email utility functions


def send_html_email(subject, html_message, recipient_list, from_email=None):
    """
    Send HTML email to a list of recipients
    """
    if from_email is None:
        from_email = settings.DEFAULT_FROM_EMAIL

    # Create plain text version of the HTML email
    plain_message = strip_tags(html_message)

    # Create email message
    email = EmailMultiAlternatives(
        subject,
        plain_message,
        from_email,
        recipient_list
    )

    # Attach HTML content
    email.attach_alternative(html_message, "text/html")

    # Send email
    success = email.send()

    return success


def send_template_email(subject, template_name, context, recipient_list, from_email=None):
    """
    Send an email using a template
    """
    # Add the subject to context
    context['subject'] = subject
    context['year'] = datetime.now().year

    # Render HTML content from template
    html_message = render_to_string(template_name, context)

    # Send the email
    return send_html_email(subject, html_message, recipient_list, from_email)

# Regular template-based views


@login_required
def send_email_to_user(request, user_id):
    """Send an email to a specific user"""
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        try:
            recipient = User.objects.get(pk=user_id)

            # Send email
            success = send_template_email(
                subject=subject,
                template_name='pack/email_template.html',
                context={'message': message},
                recipient_list=[recipient.email]
            )

            # Record the email
            EmailRecord.objects.create(
                subject=subject,
                recipient=recipient,
                was_successful=success
            )

            if success:
                messages.success(request, f"Email sent successfully to {
                                 recipient.email}")
            else:
                messages.error(request, "Failed to send email")

            return redirect('dashboard')  # Adjust to your actual URL name

        except User.DoesNotExist:
            messages.error(request, "User not found")
            return redirect('dashboard')  # Adjust to your actual URL name

    return render(request, 'pack/send_email.html', {'user_id': user_id})


@login_required
def send_bulk_email(request):
    """Send an email to multiple users"""
    if request.method == 'POST':
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        user_ids = request.POST.getlist('user_ids')

        success_count = 0
        fail_count = 0

        for user_id in user_ids:
            try:
                recipient = User.objects.get(pk=user_id)

                # Send email
                success = send_template_email(
                    subject=subject,
                    template_name='pack/email_template.html',
                    context={'message': message},
                    recipient_list=[recipient.email]
                )

                # Record the email
                EmailRecord.objects.create(
                    subject=subject,
                    recipient=recipient,
                    was_successful=success
                )

                if success:
                    success_count += 1
                else:
                    fail_count += 1

            except User.DoesNotExist:
                fail_count += 1

        messages.success(request, f"Emails sent: {
                         success_count} successful, {fail_count} failed")
        return redirect('dashboard')  # Adjust to your actual URL name

    # Get all users for the form
    users = User.objects.all()
    return render(request, 'pack/send_bulk_email.html', {'users': users})

# API views


@swagger_auto_schema(
    method='post',
    request_body=EmailSerializer,
    responses={
        200: openapi.Response('Email sent successfully', EmailSerializer),
        400: 'Bad request',
        404: 'User not found',
    },
    operation_summary="Send an email to a specific user",
    operation_description="Sends an HTML formatted email to a specific user"
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_email_to_user_api(request, user_id):
    """Send an email to a specific user"""
    serializer = EmailSerializer(data=request.data)

    if serializer.is_valid():
        subject = serializer.validated_data['subject']
        message = serializer.validated_data['message']

        try:
            recipient = User.objects.get(pk=user_id)

            # Send email
            success = send_template_email(
                subject=subject,
                template_name='pack/email_template.html',
                context={'message': message},
                recipient_list=[recipient.email]
            )

            # Record the email
            email_record = EmailRecord.objects.create(
                subject=subject,
                recipient=recipient,
                was_successful=success
            )

            if success:
                return Response(
                    {"message": f"Email sent successfully to {recipient.email}"},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {"error": "Failed to send email"},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},
                status=status.HTTP_404_NOT_FOUND
            )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method='post',
    request_body=BulkEmailSerializer,
    responses={
        200: openapi.Response('Emails sent successfully'),
        400: 'Bad request',
    },
    operation_summary="Send emails to multiple users",
    operation_description="Sends the same HTML formatted email to multiple users"
)
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_bulk_email_api(request):
    """Send an email to multiple users"""
    serializer = BulkEmailSerializer(data=request.data)

    if serializer.is_valid():
        subject = serializer.validated_data['subject']
        message = serializer.validated_data['message']
        user_ids = serializer.validated_data['user_ids']

        success_count = 0
        fail_count = 0
        failed_users = []

        for user_id in user_ids:
            try:
                recipient = User.objects.get(pk=user_id)

                # Send email
                success = send_template_email(
                    subject=subject,
                    template_name='pack/email_template.html',
                    context={'message': message},
                    recipient_list=[recipient.email]
                )

                # Record the email
                EmailRecord.objects.create(
                    subject=subject,
                    recipient=recipient,
                    was_successful=success
                )

                if success:
                    success_count += 1
                else:
                    fail_count += 1
                    failed_users.append(
                        {"id": user_id, "reason": "Email sending failed"})

            except User.DoesNotExist:
                fail_count += 1
                failed_users.append(
                    {"id": user_id, "reason": "User not found"})

        return Response({
            "message": f"Emails sent: {success_count} successful, {fail_count} failed",
            "success_count": success_count,
            "fail_count": fail_count,
            "failed_users": failed_users if failed_users else None
        }, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
