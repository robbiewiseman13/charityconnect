# Celery configuration file for the Django project.
# Sets up Celery to use Django's settings and automatically discover tasks across apps.
from __future__ import annotations
import os
from celery import Celery

# Set default Django settings module for Celery
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

# Create Celery application instance
app = Celery("backend")

# Load configuration from Django settings using the 'CELERY_' prefix
app.config_from_object("django.conf:settings", namespace="CELERY")

# Auto discover tasks from all registered Django app configs
app.autodiscover_tasks()
