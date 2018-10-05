from django.conf.urls import url

from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'dataset',  views.DatasetView)
urlpatterns = router.urls

