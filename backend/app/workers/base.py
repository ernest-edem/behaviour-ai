from app.core.celery_app import celery_app

class BaseTask:
    task = celery_app