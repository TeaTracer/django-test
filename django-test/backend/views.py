import random
import json
from rest_framework import viewsets
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.generic.edit import FormView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template import loader
from .models import Dataset
from .forms import DataForm
from .serializers import DatasetSerializer
from .celery import send_to_pipeline

#  Table with datasets
#  def table_view(request):
    #  datasets = Dataset.objects.order_by('-data_date')
    #  template = loader.get_template('table.html')
    #  context = {
        #  'datasets': datasets,
    #  }
    #  return HttpResponse(template.render(context, request))

# Run tasks
def runView(request):
    ids = Dataset.objects.values_list('id',  flat=True)
    send_to_pipeline(ids)
    n = len(ids)
    context = {
        'text': "Ok. Run {} tasks.".format(n),
    }
    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))


# Status
def status_view(request):
    failed = Dataset.objects.filter(exception__isnull=False)
    context = {
        'is_fail': bool(failed),
        'datasets': failed,
    }
    template = loader.get_template('status.html')
    return HttpResponse(template.render(context, request))

def table_view(request):
    datasets = Dataset.objects.order_by('-data_date')
    failed = Dataset.objects.filter(exception__isnull=False)

    paginator = Paginator(datasets, 10)
    page = request.GET.get('page')

    try:
        datasets = paginator.page(page)

    except PageNotAnInteger:
        datasets = paginator.page(1)

    except EmptyPage:
        datasets = paginator.page(paginator.num_pages)

    context = {
        'is_fail': bool(failed),
        'datasets': datasets,
    }
    template = loader.get_template('table.html')
    return HttpResponse(template.render(context, request))


# REST
class DatasetView(viewsets.ModelViewSet):
    queryset = Dataset.objects.all()
    serializer_class = DatasetSerializer

# Submit dataset
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
