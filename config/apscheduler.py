"""
APScheduler configuration for mmo_board project.
"""
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.django import DjangoJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from django_apscheduler.jobstores import DjangoJobStore as DjangoApschedulerJobStore
from django.conf import settings

# Create scheduler
scheduler = BackgroundScheduler(
    jobstores={
        'default': DjangoJobStore(),
        'djangojobstore': DjangoApschedulerJobStore(),
    },
    executors={
        'default': ThreadPoolExecutor(20),
    },
    job_defaults={
        'coalesce': False,
        'max_instances': 3,
    },
    timezone=settings.TIME_ZONE,
)


def start_scheduler():
    """Start the scheduler."""
    scheduler.start()


def shutdown_scheduler():
    """Shutdown the scheduler."""
    scheduler.shutdown()

