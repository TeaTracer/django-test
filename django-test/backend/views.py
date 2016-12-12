import random
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
from .models import Dataset

#  def index(request):
    #  return HttpResponse("This is app view response.")

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
    r = lambda : random.randint(10, 30)
    dataset_length = r()
    dataset_list = [[r(), r()] for _ in range(dataset_length)]
    dataset = Dataset.objects.create(data=dataset_list)
    return HttpResponse(dataset)

