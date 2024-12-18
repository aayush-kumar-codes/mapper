from datetime import datetime, timedelta
from rest_framework import serializers
from .models import FundingBase, FundingRecord, TrofiTokens
from django.db.models import Sum


class DataPointsSerializer(serializers.ModelSerializer):
    data_points = serializers.SerializerMethodField()
    class Meta:
        model = FundingRecord
        fields = ['data_points']


    def get_data_points(self, obj):
        days = self.context['day']

        tokens = TrofiTokens.objects.all()
        apy = tokens.filter(symbol=obj.future)
        try:
            data = {
                "future": obj.future,
                "flex": "" if (apy[0].apy).is_nan() else apy[0].apy
            }
        except IndexError:
            data = {
                "future": obj.future,
                "flex": ""
            }
        total_rate_list = []
        for day in days:
            # Get all the fundings of day passed in array
            try:
                fundings = FundingBase.objects.filter(future=obj.future).order_by('-time')
                fundings = fundings[0: 24*day]
            except IndexError:
                pass
            total_rate = fundings.aggregate(Sum('rate', distinct=True))
            
            try:
                rate = (total_rate['rate__sum'] / 24) * 365 * 24 * 100
                total_rate_list.append(rate)
            except TypeError:
                total_rate_list.append("")
        data["total_rate_list"] = total_rate_list
        return data
