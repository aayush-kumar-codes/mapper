from time import sleep
import ccxt
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils.timezone import get_current_timezone
import pytz
from .models import FundingBase, Future
from uuid import uuid4
from datetime import datetime, timedelta




def get_funding():
    ftx = ccxt.ftx()
    funding = ftx.publicGetFundingRates()
    result = funding['result']
    count = 0
    for item in result:
        count += 1

        if count == 20:
            sleep(3)

        future = item['future'].replace("-PERP", "")
        item_time = datetime.strptime(item['time'], '%Y-%m-%dT%H:%M:%S%z').astimezone(pytz.timezone('UTC'))
        new_time = datetime.strftime(datetime.now(), '%Y-%m-%dT%H:%M:%S')
        new_time = datetime.strptime(new_time, '%Y-%m-%dT%H:%M:%S').astimezone(pytz.timezone('UTC'))

        if ((new_time.date() != item_time.date()) or (new_time.hour != item_time.hour)):
            pass
        else:
            try:
                future_name = Future.objects.get(future=future)
                FundingBase.objects.create(id=uuid4() , future=future_name, rate=item['rate'], time=item['time'])
            except Future.DoesNotExist:
                future_name = Future.objects.create(future=future)
                FundingBase.objects.create(id=uuid4() , future=future_name, rate=item['rate'], time=item['time'])




def remove_funding_before_60_days():
    today_date = datetime.now()
    date_60_days_ago = today_date - timedelta(days=60)
    FundingBase.objects.filter(time__lt=date_60_days_ago).delete()


def Cronjob():
    scheduler = BackgroundScheduler(timezone=str(get_current_timezone()))
    scheduler.add_job(get_funding, trigger='interval', minutes=5)
    scheduler.add_job(remove_funding_before_60_days, trigger='interval', hours=24)
    scheduler.start()
