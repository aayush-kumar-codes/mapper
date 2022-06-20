from django.db import IntegrityError
import ccxt
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils.timezone import get_current_timezone
from .models import Funding, Future
from uuid import uuid4

def get_funding():
    ftx = ccxt.ftx()
    funding = ftx.publicGetFundingRates()
    result = funding['result']
    results = []
    for item in result:
        future = item['future'].replace("-PERP", "")

        try:
            future_name = Future.objects.create(future=future)
            funding_data = Funding(id=uuid4() , future=future_name, rate=item['rate'], time=item['time'])
            results.append(funding_data)
        except IntegrityError as error:
            future_name = Future.objects.get(future=future)
            funding_data = Funding(id=uuid4() , future=future_name, rate=item['rate'], time=item['time'])
            results.append(funding_data)

    Funding.objects.bulk_create(results)    


def Cronjob():
    scheduler = BackgroundScheduler(timezone=str(get_current_timezone()))
    scheduler.add_job(get_funding, trigger='interval', seconds=3600)
    scheduler.start()