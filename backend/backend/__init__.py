# Initialize Celery when Django starts
# This ensures that Celery tasks defined in the project are automatically discovered and available
from .celery import app as celery_app
__all__ = ("celery_app",)
