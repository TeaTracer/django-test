import random
import json
from rest_framework import viewsets
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
from .models import Dataset
from .serializers import DatasetSerializer

def index(request):
    datasets = Dataset.objects.order_by('-data_date')
    template = loader.get_template('index.html')
    context = {
        'datasets': datasets,
    }
    return HttpResponse(template.render(context, request))

def dataset_view(request, dataset_id):
    dataset = Dataset.objects.get(pk=dataset_id)
    return HttpResponse(dataset)

def add_random_dataset(request):
    new_dataset = json.dumps(_make_random_dataset())
    dataset = Dataset.objects.create(data=new_dataset)
    return HttpResponse(dataset)

def task(request):
    datasets = Dataset.objects.all()
    with open("tasks.log", 'a') as f:
        for dataset in datasets:
            print(dataset.id, file=f)
    return HttpResponse("Ok, " + str([dataset.id for dataset in datasets]))

class DatasetView(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer

def _make_random_dataset():
    r = lambda : random.randint(10, 30)
    dataset_length = r()
    dataset_list = [[r(), r()] for _ in range(dataset_length)]
    return dataset_list

