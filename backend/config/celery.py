import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')

from celery.schedules import crontab

app = Celery('uziel_os')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'check-expired-executions-every-minute': {
        'task': 'apps.executions.tasks.check_expired_executions_task',
        'schedule': crontab(minute='*'),
    },
    'prepare-upcoming-notifications-every-minute': {
        'task': 'apps.executions.tasks.prepare_upcoming_notifications_task',
        'schedule': crontab(minute='*'),
    },
}
