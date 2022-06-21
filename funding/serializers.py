from datetime import datetime, timedelta
from rest_framework import serializers
from .models import Funding, TrofiTokens
from django.db.models import Sum
import pandas as pd


class DataPointsSerializer(serializers.ModelSerializer):
    data_points = serializers.SerializerMethodField()
    class Meta:
        model = Funding
        fields = ['data_points']


    def get_data_points(self, obj):
        days = self.context['day']

        tokens = TrofiTokens.objects.all()
        apy = tokens.filter(symbol=obj.future)
        try:
            data = {
                "future": obj.future,
                "flex": apy[0].apy
            }
        except IndexError:
            data = {
                "future": obj.future,
                "flex": ""
            }
        total_rate_list = []
        for day in days:
            calculated_time = datetime.now() - timedelta(days=day)
            total_rate = Funding.objects.filter(time__gte=calculated_time, future=obj.future).aggregate(Sum('rate'))
            try:
                total_rate_list.append((total_rate['rate__sum'] * 365 * 24 * 100))
            except TypeError:
                total_rate_list.append("NA")
        data["total_rate_list"] = total_rate_list
        return data
