from django.shortcuts import render, redirect
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import EmailRecord

# Email sending utility functions


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

# Views


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
