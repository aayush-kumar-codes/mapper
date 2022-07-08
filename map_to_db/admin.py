from django.contrib import admin
from django.contrib.auth.models import Group

from .models import CurrencySettings

class CurrencySettingsAdmin(admin.ModelAdmin):
    list_display = [
        'currency', 
        'depo', 
        'vol_offset', 
        'ftx_feed_ticker', 
        'implied_r', 
        'spacing', 
        'maturity_factor', 
        'rounding'
    ]
    list_filter = ['currency']

# registering models
admin.site.register(CurrencySettings, CurrencySettingsAdmin)
admin.site.unregister(Group)
