from django.contrib import admin
from .models import SubscriptionPlan, Subscription, Invoice, UsageMetric


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'plan_type', 'price', 'billing_period', 'max_users', 'is_active']
    list_filter = ['plan_type', 'billing_period', 'is_active']
    search_fields = ['name', 'description']


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'status', 'current_period_start', 'current_period_end']
    list_filter = ['status', 'plan', 'created_at']
    search_fields = ['user__username', 'user__email']
    readonly_fields = ['stripe_subscription_id', 'created_at']


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['subscription', 'amount_due', 'amount_paid', 'status', 'due_date']
    list_filter = ['status', 'created_at']
    search_fields = ['subscription__user__username']
    readonly_fields = ['stripe_invoice_id', 'created_at']


@admin.register(UsageMetric)
class UsageMetricAdmin(admin.ModelAdmin):
    list_display = ['subscription', 'metric_type', 'value', 'date']
    list_filter = ['metric_type', 'date']
    search_fields = ['subscription__user__username']