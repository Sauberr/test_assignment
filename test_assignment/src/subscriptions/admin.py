from django.contrib import admin

from subscriptions.models import Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    fields = (
        "subscriber_name",
        "subscription_plan",
        "description",
        "subscription_cost",
        "paypal_subscription_id",
        "is_active",
        "user",
        "create_datetime",
        "last_update",
    )
    list_display = (
        "subscriber_name",
        "subscription_plan",
        "subscription_cost",
        "paypal_subscription_id",
        "is_active",
        "user",
    )
    list_display_links = ("subscriber_name", "subscription_plan", "subscription_cost")
    list_filter = ("subscription_plan", "is_active")
    date_hierarchy = "create_datetime"
    search_fields = ("subscriber_name", "subscription_plan", "paypal_subscription_id")
    ordering = ("create_datetime", "last_update")
    readonly_fields = ("create_datetime", "last_update")
