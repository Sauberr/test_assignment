from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.http import HttpResponse

from subscriptions.models import Subscription

from subscriptions.services.paypal import get_access_token, cancel_subscription_paypal, update_subscription_paypal, \
    get_current_subscription


def create_subscription(request, subscription_id, plan):
    user = get_user_model().objects.get(email=request.user.email)
    first_name, last_name = user.first_name, user.last_name
    full_name = f"{first_name} {last_name}"

    selected_subscription_plan = plan

    if selected_subscription_plan == 'Basic':
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


def confirm_delete_subscription(request, subscription_id):
    context = {'subscription_id': subscription_id}
    return render(request, 'subscriptions/confirm_delete_subscription.html', context)


def delete_subscription(request, subscription_id):
    access_token = get_access_token()
    cancel_subscription_paypal(access_token, subscription_id)

    subscription = Subscription.objects.get(user=request.user, paypal_subscription_id=subscription_id)
    subscription.delete()

    return render(request, 'subscriptions/delete_subscription.html')


def update_subscription(request, subscription_id: str):
    access_token = get_access_token()
    approve_link = update_subscription_paypal(access_token, subscription_id)
    if approve_link:
        return redirect(approve_link)
    else:
        return HttpResponse("Unable to obtain the approval link. Please try again later.")


def paypal_update_subscription_confirmed(request):
    try:
        subscription_details = Subscription.objects.get(user=request.user)
        subscription_id = subscription_details.paypal_subscription_id

        context = {'subscription_id': subscription_id}

        return render(request, 'subscriptions/paypal_update_subscription_confirmed.html', context)

    except:

        return render(request, 'subscriptions/paypal_update_subscription_confirmed.html')


def django_update_subscription_confirmed(request, subscription_id: str):
    access_token = get_access_token()
    current_plan_id = get_current_subscription(access_token, subscription_id)

    if current_plan_id == 'P-8E708017MM2102055M3OD57Y':
        new_plan_name: str = 'Basic'
        new_plan_cost: str = '4.99'

        Subscription.objects.filter(paypal_subscription_id=subscription_id).update(
            subscription_plan=new_plan_name,  subscription_cost=new_plan_cost
        )

    elif current_plan_id == 'P-95719217972434046M3OEGAA':
        new_plan_name: str = 'Premium'
        new_plan_cost: str = '9.99'

        Subscription.objects.filter(paypal_subscription_id=subscription_id).update(
            subscription_plan=new_plan_name,  subscription_cost=new_plan_cost
        )

    elif current_plan_id == 'P-5VS486129B569981AM3OEJXY':
        new_plan_name: str = 'Enterprise'
        new_plan_cost: str = '14.99'

        Subscription.objects.filter(paypal_subscription_id=subscription_id).update(
            subscription_plan=new_plan_name,  subscription_cost=new_plan_cost
        )

    return render(request, 'subscriptions/django_update_subscription_confirmed.html')
