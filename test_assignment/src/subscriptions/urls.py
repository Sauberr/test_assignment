from django.urls import path
from subscriptions.views import (CreateSubscription, DeleteSubscription, UpdateSubscription, \
                                 PaypalUpdateSubscriptionConfirmed, DjangoUpdateSubscriptionConfirmed, \
                                 ConfirmDeleteSubscription)


app_name: str = 'subscriptions'

urlpatterns = [
    path('create-subscription/<str:subscription_id>/<str:plan>/', CreateSubscription.as_view(), name='create_subscription'),
    path('delete-subscription/<str:subscription_id>/', ConfirmDeleteSubscription.as_view(),
         name='confirm_delete_subscription'),
    path('delete-subscription-confirmed/<str:subscription_id>/', DeleteSubscription.as_view(), name='delete_subscription'),
    path('update-subscription/<str:subscription_id>/<str:new_plan>/', UpdateSubscription.as_view(), name='update_subscription'),

    path('paypal-update-subscription-confirmed/', PaypalUpdateSubscriptionConfirmed.as_view(),
         name='paypal_update_subscription_confirmed'),
    path('django-update-subscription-confirmed/<str:subscription_id>/', DjangoUpdateSubscriptionConfirmed.as_view(),
         name='django_update_subscription_confirmed'),
]