from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from funding.views import GetTrofiToken
from funding.utils import Cronjob

urlpatterns = [
    path('admin/', admin.site.urls),
    path('funding/live-trofi-tokens/', GetTrofiToken)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

Cronjob()
