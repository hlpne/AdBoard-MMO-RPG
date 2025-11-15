"""
Tasks for newsletters app (for APScheduler).
"""
from .models import NewsletterSendJob
from .services import send_newsletter_batch


def process_newsletter_job(job_id):
    """Process a newsletter send job."""
    try:
        job = NewsletterSendJob.objects.get(pk=job_id)
        
        if job.status == NewsletterSendJob.Status.DONE:
            return
        
        # Send newsletter in batches
        send_newsletter_batch(job.template.id, batch_size=50, delay=2)
        
    except NewsletterSendJob.DoesNotExist:
        pass

