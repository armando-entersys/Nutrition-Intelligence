from celery import Celery
import os

# Create Celery instance
celery_app = Celery(
    'nutrition-intelligence',
    broker=os.getenv('REDIS_URL', 'redis://redis:6379/0'),
    backend=os.getenv('REDIS_URL', 'redis://redis:6379/0')
)

# Configuration
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

# Auto-discover tasks
celery_app.autodiscover_tasks(['tasks'])

@celery_app.task
def test_task(message: str = "Hello from Celery!"):
    """Test task to verify Celery is working"""
    return f"Task completed: {message}"