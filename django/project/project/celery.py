from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from first_part.tasks import process_message_from_rabbitmq


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

app = Celery('project')


app.conf.worker_concurrency = 1 
app.conf.pool = 'solo' 


app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
