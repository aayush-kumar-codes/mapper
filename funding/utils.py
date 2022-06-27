import ccxt
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils.timezone import get_current_timezone
import pytz
from .models import FundingBase, Future
from uuid import uuid4
from datetime import datetime, timedelta
from django.conf import settings

def get_funding():
    ftx = ccxt.ftx()
    funding = ftx.publicGetFundingRates()
    result = funding['result']
    results = []
    for item in result:
        future = item['future'].replace("-PERP", "")

        try:
            future_name = Future.objects.get(future=future)
            funding_base = FundingBase.objects.filter(future=future_name, time=datetime.strptime(item['time'], '%Y-%m-%dT%H:%M:%S%z').astimezone(pytz.timezone(settings.TIME_ZONE)))
            if not funding_base.exists():
                funding_data = FundingBase(id=uuid4() , future=future_name, rate=item['rate'], time=item['time'])
                results.append(funding_data)
        except Future.DoesNotExist:
            future_name = Future.objects.create(future=future)
            funding_data = FundingBase(id=uuid4() , future=future_name, rate=item['rate'], time=item['time'])
            results.append(funding_data)

    FundingBase.objects.bulk_create(results)    


def remove_funding_before_60_days():
    today_date = datetime.now()
    date_60_days_ago = today_date - timedelta(days=60)
    FundingBase.objects.filter(time__lt=date_60_days_ago).delete()


def Cronjob():
    scheduler = BackgroundScheduler(timezone=str(get_current_timezone()))
    scheduler.add_job(get_funding, trigger='interval', seconds=3600)
    scheduler.add_job(remove_funding_before_60_days, trigger='interval', hours=24)
    scheduler.start()
