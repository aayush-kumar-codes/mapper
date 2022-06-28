import ccxt
from apscheduler.schedulers.background import BackgroundScheduler
from django.utils.timezone import get_current_timezone
import pytz
from .models import FundingBase, Future
from uuid import uuid4
from datetime import datetime, timedelta
import logging




def get_funding():
    logging.basicConfig(level=logging.DEBUG, filename=f"logs/{str(datetime.now().date()) + str(datetime.now().time()).replace(':', '-')}.log", filemode="w", format="%(asctime)s - %(levelname)s - %(message)s")
    ftx = ccxt.ftx()
    funding = ftx.publicGetFundingRates()
    result = funding['result']
    results = []
    for item in result:
        future = item['future'].replace("-PERP", "")

        try:
            future_name = Future.objects.get(future=future)
            funding_base = FundingBase.objects.filter(future__future=future_name, time=item['time'])
            logging.debug(f"In try block funding_base = {funding_base}, future_name = {future_name}, time={item['time']}, funding_exists={funding_base.exists()}", exc_info=True)
            if not funding_base.exists():
                logging.debug("Inside ")
                funding_data = FundingBase(id=uuid4() , future=future_name, rate=item['rate'], time=item['time'])
                results.append(funding_data)
        except Future.DoesNotExist:
            logging.exception(f"In try block funding_base = {funding_base}, future_name = {future_name}, time={item['time']}, funding_exists={funding_base.exists()}", exc_info=True)
            future_name = Future.objects.create(future=future)
            funding_base = FundingBase.objects.filter(future__future=future_name, time=item['time'])
            if not funding_base.exists():
                funding_data = FundingBase(id=uuid4() , future=future_name, rate=item['rate'], time=item['time'])
            results.append(funding_data)
        logging.debug(f"RESULTS: {results}")

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
