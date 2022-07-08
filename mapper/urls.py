from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import url
from funding.views import GetTrofiToken
from funding.utils import Cronjob
from django.views.static import serve 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('funding/live-trofi-tokens/', GetTrofiToken),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
] 

Cronjob()
