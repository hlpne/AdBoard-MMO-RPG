"""
Services for accounts app.
"""
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_verification_email(user, code):
    """Send email verification code."""
    subject = 'Подтверждение регистрации на MMO Board'
    
    message = render_to_string('emails/verify_code.txt', {
        'user': user,
        'code': code,
        'site_name': 'MMO Board',
    })
    
    html_message = render_to_string('emails/verify_code.html', {
        'user': user,
        'code': code,
        'site_name': 'MMO Board',
    })
    
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        html_message=html_message,
        fail_silently=False,
    )

