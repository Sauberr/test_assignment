from django.contrib import admin

from subscriptions.models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    fields = (
        "subscription_plan",
        "subscriber_plan",
        "description",
        "subscriber_cost",
        "paypal_subscription_id",
        "is_active",
        "user",
        "create_datetime",
        "last_update",
    )
    list_display = (
        "subscriber_name",
        "subscriber_plan",
        "subscriber_cost",
        "paypal_subscription_id",
        "is_active",
        "user",
    )
    list_display_links = ("subscriber_name", "subscriber_plan", "subscriber_cost")
    list_filter = ("subscriber_plan", "is_active")
    date_hierarchy = "create_datetime"
    search_fields = ("subscriber_name", "subscriber_plan", "paypal_subscription_id")
    ordering = ("create_datetime", "last_update")
    readonly_fields = ("create_datetime", "last_update")
