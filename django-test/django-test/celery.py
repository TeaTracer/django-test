from __future__ import absolute_import
from celery import Celery
from django.conf import settings
#  from backend.models import Dataset
import os

taskdir = 'dataset_task.log'

app = Celery('tasks', backend='amqp', broker='amqp://')
#  app.config_from_object('celeryconfig')
app.autodiscover_tasks()

os.environ['DJANGO_SETTINGS_MODULE'] = "django-test.settings"

@app.task
def dataset_task(dataset_id):
    with open(taskdir, 'a') as f:
        print(dataset_id, file=f)

#  @app.task
#  def function(json_data):
    #  data = json.loads(json_data)
    #  result = sum(map(lambda x: x[0]/x[1],  data['data']))
    #  return json.dumps({'result': result})

#  @app.task
#  def read_data(dataset_id):
    #  dataset = Dataset.objects.get(pk=dataset_id)
    #  return json.dumps({'id': dataset_id, 'data': dataset.data})
