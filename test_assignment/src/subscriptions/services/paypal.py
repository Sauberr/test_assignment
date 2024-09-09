import os

import requests
import json
from typing import Dict

from subscriptions.models import Subscription


def get_access_token() -> str:
    data: Dict[str, str] = {'grant_type': 'client_credentials'}

    headers = {'Accept': 'application/json', 'Accept-Language': 'en_US'}

    client_id: str = str(os.environ.get('PAYPAL_CLIENT_ID'))
    secret_id: str = str(os.environ.get('PAYPAL_SECRET_ID'))
    url: str = 'https://api.sandbox.paypal.com/v1/oauth2/token'

    response = requests.post(url, data=data, headers=headers, auth=(client_id, secret_id)).json()
    access_token = response['access_token']

    return access_token


def cancel_subscription_paypal(access_token, subscription_id: str) -> None:
    bearer_token: str = f'Bearer {access_token}'

    headers: Dict[str, str] = {
        'Content-Type': 'application/json',
        'Authorization': bearer_token,
    }

    url: str = f'https://api.sandbox.paypal.com/v1/billing/subscriptions/{subscription_id}/cancel'

    response = requests.post(url, headers=headers)
