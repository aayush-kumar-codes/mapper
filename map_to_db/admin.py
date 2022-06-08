# import json, uuid
from django import forms
from django.contrib import admin
# from django.shortcuts import render
# from django.urls import path
# from django.http import HttpResponseRedirect
# from django.urls import reverse
# from django.contrib import messages
from django.contrib.auth.models import Group

from .models import CurrencyModel, MappingModel


class JSONImportForm(forms.Form):
    json_upload = forms.FileField()


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['currency']

class MappingModelAdmin(admin.ModelAdmin):
    list_display = ['currency', 'depo', 'vol_offset', 'FTX_feed_ticker']
    list_filter = ['currency']

    # def get_urls(self):
    #     """
    #         add custom url for admin panel
    #     """
    #     urls = super().get_urls()
    #     new_urls = [path('upload-data/', self.upload_json)]
    #     return new_urls + urls

    # def upload_json(self, request):
    #     """
    #         uploads data from json file to MappingModel
    #     """
    #     if request.method == "POST":
    #         json_file = request.FILES.get("json_upload", None)
    #         if not json_file:
    #             messages.warning(request, 'No file has been choosen')
    #             return HttpResponseRedirect(request.path_info)

    #         if not json_file.name.endswith('.json'):
    #             messages.warning(request, 'Only json file format is supported')
    #             return HttpResponseRedirect(request.path_info)
            
    #         file_data = json.loads(json_file.read().decode("utf-8"))
    #         currencies = file_data.keys()

    #         data_list = []

    #         for currency in currencies:
    #             object = file_data[currency]
    #             print(object)
    #             depo = object.get('depo', 0.0)
    #             vol_offset = object.get('offset', 0.0)
    #             FTX_feed_ticker = object.get('FTX_feed_ticker', '')

    #             try:
    #                 currency = CurrencyModel.objects.get(currency=currency)
    #             except CurrencyModel.DoesNotExist:
    #                 currency = CurrencyModel.objects.create(currency=currency)

    #             data_list.append(MappingModel(id=uuid.uuid4(), currency=currency, depo=depo, vol_offset=vol_offset, FTX_feed_ticker=FTX_feed_ticker))

    #         MappingModel.objects.bulk_create(data_list)

    #         url = reverse('admin:index')
    #         return HttpResponseRedirect(url)

    #     return render(request=request, template_name='admin/json_upload.html')

# registering models
admin.site.register(CurrencyModel, CurrencyAdmin)
admin.site.register(MappingModel, MappingModelAdmin)
admin.site.unregister(Group)