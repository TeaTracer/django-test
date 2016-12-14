from django.contrib.postgres.fields import JSONField
from django.db import models
import json


class Dataset(models.Model):
    data = JSONField()
    result = JSONField(null=True, default=None)
    exception = JSONField(null=True, default=None)
    in_process = models.BooleanField(default=False)
    data_date = models.DateTimeField('Date of dataset.', auto_now_add=True)


    def __str__(self):
        return str(self.data)
