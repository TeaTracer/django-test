from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    url(r'', include('backend.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api/',  include('backend.urls_api',  namespace='core')),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    #  urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
