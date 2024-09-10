import os

import requests
from http import HTTPStatus
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


def update_subscription_paypal(access_token, subscription_id: str) -> str:
    bearer_token: str = f'Bearer {access_token}'

    headers: Dict[str, str] = {
        'Content-Type': 'application',
        'Authorization': bearer_token,
    }

    subscriptions_details = Subscription.objects.get(paypal_subscription_id=subscription_id)
    current_subscription_plan = subscriptions_details.subscription_plan

    if current_subscription_plan == 'Basic':
        new_subscription_plan_id: str = 'P-95719217972434046M3OEGAA'

    elif current_subscription_plan == 'Premium':
        new_subscription_plan_id: str = 'P-8E708017MM2102055M3OD57Y'

    url: str = f'https://api.sandbox.paypal.com/v1/billing/subscriptions/{subscription_id}/revise'

    revision_data: Dict[str, str] = {
        'plan_id': new_subscription_plan_id,
    }

    response = requests.post(url, headers=headers, data=json.dumps(revision_data))

    response_data = response.json()

    approval_url = None

    for link in response_data.get['links', []]:
        if link.get('rel') == 'approve':
            approval_url = link['href']

    if response.status_code == HTTPStatus.OK:
        return approval_url
    else:
        return None






