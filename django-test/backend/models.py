from django.contrib.postgres.fields import ArrayField
from django.db import models


class Dataset(models.Model):
    data = ArrayField(ArrayField(models.IntegerField()))
    data_date = models.DateTimeField('Date of dataset.', auto_now_add=True)

    def __str__(self):
        return str(self.data)
