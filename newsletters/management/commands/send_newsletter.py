"""
Management command to send newsletters.
"""
from django.core.management.base import BaseCommand
from newsletters.models import NewsletterSendJob
from newsletters.services import send_newsletter_batch


class Command(BaseCommand):
    help = 'Send queued newsletter jobs'

    def add_arguments(self, parser):
        parser.add_argument(
            '--job-id',
            type=int,
            help='Process specific job ID',
        )
        parser.add_argument(
            '--batch-size',
            type=int,
            default=50,
            help='Batch size for sending (default: 50)',
        )
        parser.add_argument(
            '--delay',
            type=int,
            default=2,
            help='Delay between batches in seconds (default: 2)',
        )

    def handle(self, *args, **options):
        job_id = options.get('job_id')
        batch_size = options.get('batch_size', 50)
        delay = options.get('delay', 2)
        
        if job_id:
            # Process specific job
            try:
                job = NewsletterSendJob.objects.get(pk=job_id)
                send_newsletter_batch(job.template.id, batch_size=batch_size, delay=delay)
                self.stdout.write(self.style.SUCCESS(f'Job {job_id} processed.'))
            except NewsletterSendJob.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Job {job_id} not found.'))
        else:
            # Process all queued jobs
            queued_jobs = NewsletterSendJob.objects.filter(
                status__in=[NewsletterSendJob.Status.QUEUED, NewsletterSendJob.Status.SENDING]
            )
            
            for job in queued_jobs:
                self.stdout.write(f'Processing job {job.id}...')
                send_newsletter_batch(job.template.id, batch_size=batch_size, delay=delay)
                self.stdout.write(self.style.SUCCESS(f'Job {job.id} processed.'))
            
            if not queued_jobs.exists():
                self.stdout.write(self.style.WARNING('No queued jobs found.'))

