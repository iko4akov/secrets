from datetime import datetime

from celery import shared_task

from secret.models import Secret


@shared_task
def burning_secret():
    """
    Celery task that deletes secrets with a 'date_of_burning'
    earlier than the current date and time.
    This task queries the 'Secret' model for secrets with a
    'date_of_burning' earlier than the current date
    and deletes them.

    """
    secrets = Secret.objects.filter(date_of_burning__lt=datetime.now()).all()
    if secrets:
        for secret in secrets:
            secret.delete()
