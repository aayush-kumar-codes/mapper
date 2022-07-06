from time import sleep
import ccxt
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils.timezone import get_current_timezone
import pytz

from funding.views import GetTrofiToken, GetTrofiTokenDev, GetTrofiTokenStaging
from .models import FundingBase, Future ,CRON
from uuid import uuid4
from datetime import datetime, timedelta




def get_funding():
    new_time = datetime.strftime(datetime.now(), '%Y-%m-%dT%H:%M:%S')
    new_time = datetime.strptime(new_time, '%Y-%m-%dT%H:%M:%S').astimezone(pytz.timezone('UTC'))
    cron_setting = CRON.objects.all()
    if cron_setting:
        cron_hour = cron_setting.first()
        if cron_hour.hour == new_time.hour:
            return
        else:
            cron_hour.hour = new_time.hour
            cron_hour.save()
    else:
        CRON.objects.create(hour=new_time.hour)
    ftx = ccxt.ftx()
    funding = ftx.publicGetFundingRates()
    result = funding['result']
    results = []
    for item in result:

        future = item['future'].replace("-PERP", "")
        item_time = datetime.strptime(item['time'], '%Y-%m-%dT%H:%M:%S%z').astimezone(pytz.timezone('UTC'))

        if ((new_time.date() != item_time.date()) or (new_time.hour != item_time.hour)):
            pass
        else:
            try:
                future_name = Future.objects.get(future=future)
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
    scheduler.add_job(get_funding, trigger='interval', minutes=30)
    scheduler.add_job(remove_funding_before_60_days, trigger='interval', hours=24)
    scheduler.add_job(GetTrofiToken, trigger='interval', hours=24)
    scheduler.add_job(GetTrofiTokenDev, trigger='interval', hours=24)
    scheduler.add_job(GetTrofiTokenStaging, trigger='interval', hours=24)
    scheduler.start()
