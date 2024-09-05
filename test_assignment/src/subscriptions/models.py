from django.core.validators import MinLengthValidator, MinValueValidator
from django.db import models

from account.models import User


class Subscription(models.Model):
    subscriber_name = models.CharField(max_length=255, validators=[MinLengthValidator(2)])
    subscriber_plan = models.CharField(max_length=255, validators=[MinLengthValidator(2)])
    description = models.TextField(max_length=1024, null=True, blank=True)
    subscriber_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00, validators=[MinValueValidator(0.00)]
    )
    paypal_subscription_id = models.CharField(max_length=300, null=True, blank=True)
    is_active = models.BooleanField(default=False)
    create_datetime = models.DateTimeField(auto_now_add=True, null=True)
    last_update = models.DateTimeField(auto_now=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, unique=True)

    def __str__(self):
        return f"{self.subscriber_name} - {self.subscriber_plan} subscription"

    class Meta:
        verbose_name: str = "Subscription"
        verbose_name_plural: str = "Subscriptions"
