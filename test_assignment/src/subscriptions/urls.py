from django.urls import path
from subscriptions.views import create_subscription


app_name = "subscriptions"

urlpatterns = [
    path('create-subscription/<str:subid>/<str:plan>/', create_subscription, name='create_subscription'),
]