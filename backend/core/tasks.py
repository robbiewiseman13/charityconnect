# Celery task definitions for asynchronous background processing
# Provides example task used to verify Celery is correctly configured and running

from celery import shared_task

@shared_task
def ping():
    return "pong"

