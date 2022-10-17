from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls import url
from funding.views import GetTrofiToken
from funding_dev.views import GetTrofiTokenDev
from funding_staging.views import GetTrofiTokenStaging
from .utils import Cronjob
from django.views.static import serve 

admin.site.site_header = "Trofi Admin"
admin.site.site_title = "Trofi Admin"
admin.site.index_title = "Trofi Risk Management Panel"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('funding/live-trofi-tokens/', GetTrofiToken),
    path('funding/dev-trofi-tokens/', GetTrofiTokenDev),
    path('funding/staging-trofi-tokens/', GetTrofiTokenStaging),
    url(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}), 
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
] 

Cronjob()
