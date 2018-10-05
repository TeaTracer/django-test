from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.table_view, name='table'),
    url(r'^dataform$', views.DataformView.as_view(), name='dataform'),
    #  url(r'^dataform$', views.dataform_view, name='dataform'),
    url(r'^table$', views.table_view, name='table'),
    url(r'^status$', views.status_view, name='status'),
    url(r'^run$', views.runView, name='run'),
]
