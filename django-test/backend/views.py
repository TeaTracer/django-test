import random
import json
from rest_framework import viewsets
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
from .models import Dataset
from .forms import DataForm
from .serializers import DatasetSerializer
from .celery import send_to_pipeline

def table_view(request):
    datasets = Dataset.objects.order_by('-data_date')
    template = loader.get_template('table.html')
    context = {
        'datasets': datasets,
    }
    return HttpResponse(template.render(context, request))

def add_random_dataset(request):
    dataset_d = json.dumps(_make_random_dataset())
    dataset = Dataset.objects.create(data=dataset_d)
    return HttpResponse(dataset)

# REST
class DatasetView(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer

def runView(request):
    ids = Dataset.objects.values_list('id',  flat=True)
    send_to_pipeline(ids)
    return redirect('table')

def _make_random_dataset():
    r = lambda : random.randint(10, 30)
    dataset_length = r()
    dataset_list = [[r(), r()] for _ in range(dataset_length)]
    return dataset_list

from django.views.generic.edit import FormView

class DataformView(FormView):
    form_class = DataForm
    template_name = "dataform.html"
    success_url = '/table'

    def form_valid(self, form):
        numbers = list(map(int, form.cleaned_data['data']))
        pairs = list(zip(numbers[::2],  numbers[1::2]))
        dataset = json.dumps(pairs)
        Dataset.objects.create(data=dataset)
        return redirect('table')

    def form_invalid(self, form):
        return redirect('dataform')
