from __future__ import absolute_import
import os
import time
import json
from celery import Celery, chain
from django.conf import settings

os.environ['DJANGO_SETTINGS_MODULE'] = "django-test.settings"
import django
django.setup()

app = Celery('tasks', backend='amqp', broker='amqp://')
app.config_from_object('django.conf:settings',  namespace='CELERY')
app.autodiscover_tasks()

from .models import Dataset

def send_to_pipeline(dataset_ids):
    for dataset_id in dataset_ids:
        chain(create_json_request.s(dataset_id), do_task.s(), save_result.s()).apply_async()

@app.task
def do_task(json_data):
    try:
        data = json.loads(json_data)
        time.sleep(5)
        result = sum(map(lambda x: x[0]/x[1],  data['data']))
    except Exception as error:
        return json.dumps({'id': data['id'], 'exception': repr(error), 'in_process': False})

    return json.dumps({'id': data['id'], 'result': result, 'in_process': False})

@app.task
def create_json_request(dataset_id):
    dataset = Dataset.objects.get(pk=dataset_id)
    dataset.in_process= True
    dataset.save()
    return json.dumps({'id': dataset_id, 'data': json.loads(dataset.data)})

@app.task
def save_result(json_data):
    result_dict = json.loads(json_data)
    Dataset.objects.update_or_create(pk=result_dict['id'], defaults=result_dict)
