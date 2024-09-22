from django.urls import path
from subscriptions.views import (create_subscription, delete_subscription, update_subscription,
                                 paypal_update_subscription_confirmed, django_update_subscription_confirmed,
                                 ConfirmDeleteSubscription)


app_name: str = 'subscriptions'

urlpatterns = [
    path('create-subscription/<str:subscription_id>/<str:plan>/', create_subscription, name='create_subscription'),
    path('delete-subscription/<str:subscription_id>/', ConfirmDeleteSubscription.as_view(),
         name='confirm_delete_subscription'),
    path('delete-subscription-confirmed/<str:subscription_id>/', delete_subscription, name='delete_subscription'),
    path('update-subscription/<str:subscription_id>/<str:new_plan>/', update_subscription, name='update_subscription'),

    path('paypal-update-subscription-confirmed/', paypal_update_subscription_confirmed,
         name='paypal_update_subscription_confirmed'),
    path('django-update-subscription-confirmed/<str:subscription_id>/', django_update_subscription_confirmed,
         name='django_update_subscription_confirmed'),
]