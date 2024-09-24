from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views import View

from django.views.generic import DeleteView

from account.services.mixins import TitleMixin
from subscriptions.models import Subscription

from subscriptions.services.paypal import get_access_token, cancel_subscription_paypal, update_subscription_paypal, \
    get_current_subscription


def create_subscription(request, subscription_id: str, plan: str) -> HttpResponse:
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

    context = {'subscription_plan': selected_subscription_plan, 'title': 'Subscription Created'}

    return render(request, 'subscriptions/create_subscription.html', context)


class ConfirmDeleteSubscription(LoginRequiredMixin, TitleMixin, DeleteView):
    model = Subscription
    template_name: str = 'subscriptions/confirm_delete_subscription.html'
    success_url = reverse_lazy('subscriptions:delete_subscription')
    slug_field: str = 'paypal_subscription_id'
    slug_url_kwarg: str = 'subscription_id'
    title = 'Confirm Subscription Deletion'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['subscription_id'] = self.kwargs['subscription_id']
        return context


class DeleteSubscription(LoginRequiredMixin, TitleMixin, View):

    def get(self, request, subscription_id: str) -> HttpResponse:
        access_token = get_access_token()
        cancel_subscription_paypal(access_token, subscription_id)

        subscription = Subscription.objects.get(user=request.user, paypal_subscription_id=subscription_id)
        subscription.delete()
        context = {'title': 'Subscription Deleted'}

        return render(request, 'subscriptions/delete_subscription.html', context)


class UpdateSubscription(View):

    def get(self, request, subscription_id: str, new_plan: str) -> HttpResponse:
        access_token = get_access_token()
        approve_link = update_subscription_paypal(access_token, subscription_id, new_plan)
        if approve_link:
            return redirect(approve_link)
        else:
            return HttpResponse("Unable to obtain the approval link. Please try again later.")


class PaypalUpdateSubscriptionConfirmed(View):

    def get(self, request, *args, **kwargs) -> HttpResponse:
        try:
            subscription_details = Subscription.objects.get(user=request.user)
            subscription_id = subscription_details.paypal_subscription_id

            context = {'subscription_id': subscription_id}
            return render(request, 'subscriptions/paypal_update_subscription_confirmed.html', context)
        except Subscription.DoesNotExist:
            return render(request, 'subscriptions/paypal_update_subscription_confirmed.html')


def django_update_subscription_confirmed(request, subscription_id: str) -> HttpResponse:
    access_token = get_access_token()
    current_plan_id = get_current_subscription(access_token, subscription_id)

    if current_plan_id == 'P-6GS86287F0539600CM3YD7OQ':
        new_plan_name: str = 'Basic'
        new_plan_cost: str = '4.99'

        Subscription.objects.filter(paypal_subscription_id=subscription_id).update(
            subscription_plan=new_plan_name,  subscription_cost=new_plan_cost
        )

    elif current_plan_id == 'P-7KE47576DG258030BM3YEAFA':
        new_plan_name: str = 'Premium'
        new_plan_cost: str = '9.99'

        Subscription.objects.filter(paypal_subscription_id=subscription_id).update(
            subscription_plan=new_plan_name,  subscription_cost=new_plan_cost
        )

    elif current_plan_id == 'P-3WE528458D9215156M3YEAMI':
        new_plan_name: str = 'Enterprise'
        new_plan_cost: str = '14.99'

        Subscription.objects.filter(paypal_subscription_id=subscription_id).update(
            subscription_plan=new_plan_name,  subscription_cost=new_plan_cost
        )

    return render(request, 'subscriptions/django_update_subscription_confirmed.html')
