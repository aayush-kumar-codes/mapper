from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group

from .models import CurrencyModel, MappingModel


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ['currency']

class MappingModelAdmin(admin.ModelAdmin):
    list_display = ['currency', 'depo', 'vol_offset', 'FTX_feed_ticker']
    list_filter = ['currency']

# registering models
admin.site.register(CurrencyModel, CurrencyAdmin)
admin.site.register(MappingModel, MappingModelAdmin)
admin.site.unregister(Group)