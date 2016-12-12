from django.contrib.postgres.fields import JSONField
from django.db import models


class Data(models.Model):
    data = JSONField()
    data_date = models.DateTimeField('Date of dataset.')
