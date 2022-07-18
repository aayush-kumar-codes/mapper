from datetime import datetime, timedelta, timezone
import requests, pytz

from django.contrib import admin
from django.contrib.auth.models import Group
from django.conf import settings
from django.urls import path
from django.shortcuts import render

from .models import CurrencySettings, OptionsFixingPrice

utc=pytz.UTC

time = datetime.utcnow()
time_obj = datetime.now()

t = datetime(time_obj.year, time_obj.month, time_obj.day, 8, 00, 00, 00, tzinfo=timezone.utc)

if utc.localize(time) < t:
    start_date = datetime.now().date() - timedelta(days=1)
else:
    start_date = datetime.now().date()

day_0 = str(start_date)
day_1 = str(start_date - timedelta(days=1))
day_2 = str(start_date - timedelta(days=2))
day_3 = str(start_date - timedelta(days=3))
day_4 = str(start_date - timedelta(days=4))
day_5 = str(start_date - timedelta(days=5))
day_6 = str(start_date - timedelta(days=6))
day_7 = str(start_date - timedelta(days=7))
day_8 = str(start_date - timedelta(days=8))
day_9 = str(start_date - timedelta(days=9))
day_10 = str(start_date - timedelta(days=10))
day_11 = str(start_date - timedelta(days=11))
day_12 = str(start_date - timedelta(days=12))
day_13 = str(start_date - timedelta(days=13))
day_14 = str(start_date - timedelta(days=14))
day_15 = str(start_date - timedelta(days=15))
day_16 = str(start_date - timedelta(days=16))
day_17 = str(start_date - timedelta(days=17))
day_18 = str(start_date - timedelta(days=18))
day_19 = str(start_date - timedelta(days=19))
day_20 = str(start_date - timedelta(days=20))
day_21 = str(start_date - timedelta(days=21))
day_22 = str(start_date - timedelta(days=22))
day_23 = str(start_date - timedelta(days=23))
day_24 = str(start_date - timedelta(days=24))
day_25 = str(start_date - timedelta(days=25))
day_26 = str(start_date - timedelta(days=26))
day_27 = str(start_date - timedelta(days=27))
day_28 = str(start_date - timedelta(days=28))
day_29 = str(start_date - timedelta(days=29))


choices = [
            {"name": day_0, "display": day_0},
            {"name": day_1, "display": day_1},
            {"name": day_2, "display": day_2},
            {"name": day_3, "display": day_3},
            {"name": day_4, "display": day_4},
            {"name": day_5, "display": day_5},
            {"name": day_6, "display": day_6},
            {"name": day_7, "display": day_7},
            {"name": day_8, "display": day_8},
            {"name": day_9, "display": day_9},
            {"name": day_10, "display": day_10},
            {"name": day_11, "display": day_11},
            {"name": day_12, "display": day_12},
            {"name": day_13, "display": day_13},
            {"name": day_14, "display": day_14},
            {"name": day_15, "display": day_15},
            {"name": day_16, "display": day_16},
            {"name": day_17, "display": day_17},
            {"name": day_18, "display": day_18},
            {"name": day_19, "display": day_19},
            {"name": day_20, "display": day_20},
            {"name": day_21, "display": day_21},
            {"name": day_22, "display": day_22},
            {"name": day_23, "display": day_23},
            {"name": day_24, "display": day_24},
            {"name": day_25, "display": day_25},
            {"name": day_26, "display": day_26},
            {"name": day_27, "display": day_27},
            {"name": day_28, "display": day_28},
            {"name": day_29, "display": day_29},
]
    
            
class OptionsFixingPriceAdmin(admin.ModelAdmin):

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

    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('options-fixing-price/', self.options_fixing_price)]
        return new_urls + urls

    def options_fixing_price(self, request):
        currencies = CurrencySettings.objects.values_list("currency")
        fixes_list = []
        date = request.GET.get('date', None)
        if date is None and utc.localize(time) < t:
            date = datetime.now().date() - timedelta(days=1)
        elif date is None:
            date = datetime.now().date()
        for currency in currencies:
            response = requests.get(url=f'{settings.TROFI_PRICE_URL}/?date={date}&currency={currency[0]}')
            if response.status_code == 200:
                fixes_list.append({"currency": currency[0], "price": response.json()["data"]["index_price"]})
            else:
                fixes_list.append({"currency": currency[0], "price": ""})

        return render(request=request, template_name='admin/map_to_db/optionsfixingprice/options-fixes-price.html', context={"fixes": fixes_list, "choices": choices, "title": "Date Filter"})

# registering models
admin.site.register(OptionsFixingPrice, OptionsFixingPriceAdmin)
admin.site.unregister(Group)
