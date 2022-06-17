from fastapi import APIRouter, HTTPException
import os
import requests

from app.core import request
from app.schemas.rate import Rate

router = APIRouter()

@router.get('/rates/{currency}', response_model=Rate)
async def get_rates(currency):
    if currency not in ['JPY', 'USD', 'EUR']:
        raise HTTPException(status_code=404, detail='only "JPY", "USD" or "EUR" are supported.')

    if os.getenv('EXCHANGERATE_API_URL') is None:
        raise HTTPException(status_code=500, detail='Something went wrong with my settings...')

    try:
        url = '{0}/{1}'.format(os.getenv('EXCHANGERATE_API_URL'), currency)
        response = requests.request('GET', url)
        rates = response.json()['rates']
        return response.json()

    except Exception as error:
        raise HTTPException(status_code=500, detail=error.message)
