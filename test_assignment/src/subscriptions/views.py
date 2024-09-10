from django.contrib.auth import get_user_model
from django.shortcuts import render

from subscriptions.models import Subscription

from subscriptions.services.paypal import get_access_token, cancel_subscription_paypal


def create_subscription(request, subscription_id, plan):
    user = get_user_model().objects.get(email=request.user.email)
    first_name, last_name = user.first_name, user.last_name
    full_name = f"{first_name} {last_name}"

    selected_subscription_plan = plan

    if selected_subscription_plan == "Basic":
        subscriptions_cost = "4.99"
    elif selected_subscription_plan == "Premium":
        subscriptions_cost = "9.99"
    elif selected_subscription_plan == "Enterprise":
        subscriptions_cost = "14.99"

    subscriptions = Subscription.objects.create(
        subscriber_name=full_name,
        subscription_plan=selected_subscription_plan,
        subscription_cost=subscriptions_cost,
        paypal_subscription_id=subscription_id,
        is_active=True,
        user=request.user
    )

    context = {'subscription_plan': selected_subscription_plan}

    return render(request, 'subscriptions/create_subscription.html', context)


def delete_subscription(request, subscription_id):
    access_token = get_access_token()
    cancel_subscription_paypal(access_token, subscription_id)

    subscription = Subscription.objects.get(user=request.user, paypal_subscription_id=subscription_id)
    subscription.delete()

    return render(request, 'subscriptions/delete_subscription.html')


def update_subscription(request, subscription_id):
    ...
