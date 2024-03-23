import os

from celery import Celery


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'truck_search.settings')

app = Celery('truck_search')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'update_locations': {
        'task': 'trucks.tasks.update_locations',
        'schedule': 180.0,
    },
}
