from uuid import uuid4
import ccxt, requests
from django.conf import settings
from django.http import JsonResponse
from .models import FundingBase
import pandas as pd
from .models import TrofiTokens, TrofiTokensDev, TrofiTokensStaging


ftx = ccxt.ftx()

def GetFunding(request):
    funding = ftx.publicGetFundingRates()
    result = funding['result']
    results = []

    results = [FundingBase(future=item['future'].replace("-PERP", ""), rate=item['rate'], time=item['time']) for item in result]

    FundingBase.objects.bulk_create(results)    

    return JsonResponse({})

def GetTrofiToken(request=None):
    response = requests.get(
            url=settings.TROFI_URL,
            headers={
                "trofi-secret": settings.TROFI_SECRET
            }
        )

    data = response.json()['flexibleEarn']
    df = pd.json_normalize(data)
    FIELDS = ["apy", "token.symbol", "is_active", "token._id", "token.priority"]
    df = df[FIELDS]

    tokens_list = df.values
    trofi_token_list = []
    for token in tokens_list:
        trofi_token = TrofiTokens.objects.filter(symbol=token[1])
        if trofi_token.exists():
            trofi_token_instance = trofi_token[0]
            trofi_token_instance.apy = token[0]
            trofi_token_instance.is_active = token[2]
            trofi_token_instance.token_id = token[3]
            trofi_token_instance.priority = token[4] if str(token[4]) != "nan" else ''
            trofi_token_instance.save()
        else:
            trofi_token_list.append(
                TrofiTokens(
                    id=uuid4(),
                    apy=token[0],
                    symbol=token[1],
                    is_active=token[2],
                    token_id=token[3],
                    priority=token[4] if str(token[4]) != "nan" else ''
                )
            )
    if len(trofi_token_list) != 0:
        TrofiTokens.objects.bulk_create(
            trofi_token_list
        )
    
    return JsonResponse({"status": 200})


def GetTrofiTokenDev():
    response = requests.get(
            url=settings.TROFI_DEV_URL,
            headers={
                "trofi-secret": settings.TROFI_DEV_SECRET
            }
        )

    data = response.json()['flexibleEarn']
    df = pd.json_normalize(data)
    FIELDS = ["apy", "token.symbol", "is_active", "token._id", "token.priority"]
    df = df[FIELDS]

    tokens_list = df.values
    trofi_token_list = []
    for token in tokens_list:
        trofi_token = TrofiTokensDev.objects.filter(symbol=token[1])
        if trofi_token.exists():
            trofi_token[0].apy = token[0]
            trofi_token[0].is_active = token[2]
            trofi_token[0].token_id = token[3]
            trofi_token[0].priority = token[4] if str(token[4]) != "nan" else ''
            trofi_token[0].save()
        else:
            trofi_token_list.append(
                TrofiTokensDev(
                    id=uuid4(),
                    apy=token[0],
                    symbol=token[1],
                    is_active=token[2],
                    token_id=token[3],
                    priority=token[4] if str(token[4]) != "nan" else ''
                )
            )
    if len(trofi_token_list) != 0:
        TrofiTokensDev.objects.bulk_create(
            trofi_token_list
        )
    
    return JsonResponse({"status": 200})


def GetTrofiTokenStaging():
    response = requests.get(
            url=settings.TROFI_STAGING_URL,
            headers={
                "trofi-secret": settings.TROFI_STAGING_SECRET
            }
        )

    data = response.json()['flexibleEarn']
    df = pd.json_normalize(data)
    FIELDS = ["apy", "token.symbol", "is_active", "token._id", "token.priority"]
    df = df[FIELDS]

    tokens_list = df.values
    trofi_token_list = []
    for token in tokens_list:
        trofi_token = TrofiTokensStaging.objects.filter(symbol=token[1])
        if trofi_token.exists():
            trofi_token[0].apy = token[0]
            trofi_token[0].is_active = token[2]
            trofi_token[0].token_id = token[3]
            trofi_token[0].priority = token[4] if str(token[4]) != "nan" else ''
            trofi_token[0].save()
        else:
            trofi_token_list.append(
                TrofiTokensStaging(
                    id=uuid4(),
                    apy=token[0],
                    symbol=token[1],
                    is_active=token[2],
                    token_id=token[3],
                    priority=token[4] if str(token[4]) != "nan" else ''
                )
            )
    if len(trofi_token_list) != 0:
        TrofiTokensStaging.objects.bulk_create(
            trofi_token_list
        )
    
    return JsonResponse({"status": 200})