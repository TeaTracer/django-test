import random
import json
from rest_framework import viewsets
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
from .models import Dataset
from .serializers import DatasetSerializer

def table_view(request):
    datasets = Dataset.objects.order_by('-data_date')
    template = loader.get_template('table.html')
    context = {
        'datasets': datasets,
    }
    return HttpResponse(template.render(context, request))

def add_random_dataset(request):
    new_dataset = json.dumps(_make_random_dataset())
    dataset = Dataset.objects.create(data=new_dataset)
    return HttpResponse(dataset)

# REST
class DatasetView(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer

def _make_random_dataset():
    r = lambda : random.randint(10, 30)
    dataset_length = r()
    dataset_list = [[r(), r()] for _ in range(dataset_length)]
    return dataset_list

def dataform_view(request):
   dataset = []
   if request.method == "POST":
      dataForm = DataForm(request.POST)
      if dataForm.is_valid():
         dataset = dataForm.cleaned_data['data']
   else:
      MyLoginForm = DataForm()
   return render(request, 'dataform.html')

