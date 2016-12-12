from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<dataset_id>[0-9]+)/$', views.dataset_view, name='dataset_view'),
    url(r'^add_random$', views.add_random_dataset, name='add_random_dataset'),
]
