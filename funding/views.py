from uuid import uuid4
import ccxt, requests
from django.http import JsonResponse
from .models import Funding
import pandas as pd
from .models import TrofiTokens


ftx = ccxt.ftx()

def GetFunding(request):
    funding = ftx.publicGetFundingRates()
    result = funding['result']
    results = []

    results = [Funding(future=item['future'].replace("-PERP", ""), rate=item['rate'], time=item['time']) for item in result]

    Funding.objects.bulk_create(results)    

    return JsonResponse({})

def GetTrofiToken(request):
    response = requests.get(
            url="https://api.trofi.group/user/earn/earn-public?detailType=flexible",
            headers={
                "trofi-secret": "832bf965e131x9"
            }
        )

    data = response.json()['flexibleEarn']
    df = pd.json_normalize(data)
    FIELDS = ["apy", "token.symbol", "is_active"]
    df = df[FIELDS]

    tokens_list = df.values
    trofi_token_list = []
    for token in tokens_list:
        trofi_token = TrofiTokens.objects.filter(symbol=token[1])
        if trofi_token.exists():
            trofi_token[0].apy = token[0]
            trofi_token[0].is_active = token[2]
            trofi_token[0].save()
        else:
            trofi_token_list.append(
                TrofiTokens(
                    id=uuid4(),
                    apy=token[0],
                    symbol=token[1],
                    is_active=token[2]
                )
            )
    TrofiTokens.objects.bulk_create(
        trofi_token_list
    )
    
    return JsonResponse({"status": 200})