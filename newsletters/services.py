"""
Services for newsletters app.
"""
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils import timezone
from .models import Subscription, NewsletterTemplate, NewsletterSendJob


def subscribe_user(user):
    """Subscribe user to newsletter."""
    subscription, created = Subscription.objects.get_or_create(
        user=user,
        defaults={'is_active': True}
    )
    if not created:
        subscription.is_active = True
        subscription.save()
    return subscription


def unsubscribe_user(user):
    """Unsubscribe user from newsletter."""
    try:
        subscription = Subscription.objects.get(user=user)
        subscription.is_active = False
        subscription.save()
        return subscription
    except Subscription.DoesNotExist:
        return None


def send_newsletter_batch(template_id, batch_size=50, delay=2):
    """
    Send newsletter in batches.
    """
    import time
    
    template = NewsletterTemplate.objects.get(pk=template_id)
    
    # Get active subscriptions
    subscriptions = Subscription.objects.filter(is_active=True).select_related('user')
    total = subscriptions.count()
    
    # Create or get send job
    job, created = NewsletterSendJob.objects.get_or_create(
        template=template,
        status__in=[NewsletterSendJob.Status.QUEUED, NewsletterSendJob.Status.SENDING],
        defaults={
            'status': NewsletterSendJob.Status.QUEUED,
            'total': total
        }
    )
    
    if not created:
        job.total = total
        job.save()
    
    if job.status == NewsletterSendJob.Status.QUEUED:
        job.status = NewsletterSendJob.Status.SENDING
        job.started_at = timezone.now()
        job.save()
    
    # Send in batches
    sent = job.sent
    errors = job.errors
    
    for i in range(sent, total, batch_size):
        batch = subscriptions[i:i + batch_size]
        
        for subscription in batch:
            try:
                send_mail(
                    subject=template.title,
                    message='',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[subscription.user.email],
                    html_message=template.html_body,
                    fail_silently=False,
                )
                sent += 1
            except Exception as e:
                errors += 1
                # Log error
                import logging
                logger = logging.getLogger('newsletters')
                logger.error(f'Error sending newsletter to {subscription.user.email}: {e}')
        
        # Update job progress
        job.sent = sent
        job.errors = errors
        job.save()
        
        # Delay between batches
        if i + batch_size < total:
            time.sleep(delay)
    
    # Mark job as done
    job.status = NewsletterSendJob.Status.DONE if errors == 0 else NewsletterSendJob.Status.FAILED
    job.finished_at = timezone.now()
    job.save()
    
    return job

