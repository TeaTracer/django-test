from __future__ import absolute_import
from celery import Celery
from django.conf import settings
import os

taskdir = 'dataset_task.log'

app = Celery('tasks', backend='amqp', broker='amqp://')
app.autodiscover_tasks()

os.environ[ 'DJANGO_SETTINGS_MODULE' ] = "django-test.settings"

@app.task
def dataset_task(dataset_id):
    with open(taskdir, 'a') as f:
        print(dataset_id, file=f)
