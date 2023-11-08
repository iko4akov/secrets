from datetime import datetime

from celery import shared_task

from secret.models import Secret

@shared_task
def burning_secret():

    secrets = Secret.objects.filter(date_of_burning__lt=datetime.now()).all()

    if secrets:
        for secret in secrets:
            secret.delete()


