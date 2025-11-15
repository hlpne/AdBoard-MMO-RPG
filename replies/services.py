"""
Services for replies app.
"""
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


def send_reply_notification(reply):
    """Send email notification to advert author when a new reply is created."""
    advert = reply.advert
    author = advert.author
    
    subject = f'Новый отклик на ваше объявление: {advert.title}'
    
    message = render_to_string('emails/reply_notice.txt', {
        'advert': advert,
        'reply': reply,
        'site_name': 'MMO Board',
    })
    
    html_message = render_to_string('emails/reply_notice.html', {
        'advert': advert,
        'reply': reply,
        'site_name': 'MMO Board',
    })
    
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[author.email],
        html_message=html_message,
        fail_silently=False,
    )


def send_accept_notification(reply):
    """Send email notification to reply author when reply is accepted."""
    reply_author = reply.author
    advert = reply.advert
    
    subject = f'Ваш отклик принят: {advert.title}'
    
    message = render_to_string('emails/accept_notice.txt', {
        'advert': advert,
        'reply': reply,
        'site_name': 'MMO Board',
    })
    
    html_message = render_to_string('emails/accept_notice.html', {
        'advert': advert,
        'reply': reply,
        'site_name': 'MMO Board',
    })
    
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[reply_author.email],
        html_message=html_message,
        fail_silently=False,
    )

