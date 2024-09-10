from django.urls import path
from subscriptions.views import create_subscription, delete_subscription, update_subscription


app_name: str = "subscriptions"

urlpatterns = [
    path('create-subscription/<str:subscription_id>/<str:plan>/', create_subscription, name='create_subscription'),
    path('delete-subscription/<str:subscription_id>/', delete_subscription, name='delete_subscription'),
    path('update-subscription/<str:subscription_id>/', delete_subscription, name='update_subscription'),
]