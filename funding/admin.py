from django.contrib import admin
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from settings.models import Settings

from .models import Funding, FundingProxy, Future, TrofiTokens
from django.urls import path

from .serializers import DataPointsSerializer


class HistoryFilter(admin.SimpleListFilter):
    """
        filters the funding table on basis of history of storing
    """
    title = 'Funding History Filter'
    parameter_name = 'time'

    def lookups(self, request, model_admin):
        return (
            ('Today', _('Today')),
            ('Last One Week', _('Last One Week')),
            ('1 Month', _('1 Month')),
            ('1 Year', _('1 Year')),
            ('2 Year', _('2 Year')),
            ('3 Year', _('3 Year')),
            ('5 Year', _('5 Year'))
        )

    def queryset(self, request, queryset):
        if self.value() == 'Today':
            return queryset.filter(time__date=datetime.now().date())
        if self.value() == 'Last One Week':
            last_week = datetime.now() - timedelta(days=7)
            return queryset.filter(time__lte=datetime.now(), time__gte=last_week)
        if self.value() == '1 Month':
            today = datetime.now().today()
            first = today.replace(day=1)
            last_month = first - timedelta(days=1)
            return queryset.filter(time__gt=last_month, time__lte=datetime.now())
        if self.value() == '1 Year':
            last_year = (datetime.now()-relativedelta(years=1))
            return queryset.filter(time__gt=last_year, time__lte=datetime.now())
        if self.value() == '2 Year':
            last_2_year = (datetime.now()-relativedelta(years=2))
            return queryset.filter(time__gt=last_2_year, time__lte=datetime.now())
        if self.value() == '3 Year':
            last_3_year = (datetime.now()-relativedelta(years=3))
            return queryset.filter(time__gt=last_3_year, time__lte=datetime.now())
        if self.value() == '5 Year':
            last_5_year = (datetime.now()-relativedelta(years=5))
            return queryset.filter(time__gt=last_5_year, time__lte=datetime.now())


class FundingAdmin(admin.ModelAdmin):
    list_display = ['future', 'rate', 'time']
    list_filter = ['future', HistoryFilter]


class DataPointsAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        new_urls = [path('data-points/', self.get_data_points)]
        return new_urls + urls

    def get_data_points(self, request):
        list_of_days = Settings.objects.first().days
        funding_future = Future.objects.all()
        serialized_data = DataPointsSerializer(funding_future, many=True, context={"day": list_of_days, "dataframe": ""})
        return render(request=request, template_name='admin/funding/fundingproxy/data_points_list.html', context={"content_title": "Funding Data Points", "data_points": serialized_data.data, "days": list_of_days})



admin.site.register(Funding, FundingAdmin)
admin.site.register(FundingProxy, DataPointsAdmin)
admin.site.register(TrofiTokens)
admin.site.register(Future)