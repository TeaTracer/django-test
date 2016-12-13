from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^task$', views.task, name='task'),
    url(r'^add_random$', views.add_random_dataset, name='add_random_dataset'),
]
