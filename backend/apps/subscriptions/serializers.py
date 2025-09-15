from rest_framework import serializers
from .models import SubscriptionPlan, Subscription, Invoice, UsageMetric


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = ['id', 'name', 'plan_type', 'description', 'price',
                 'billing_period', 'max_users', 'max_storage_gb', 'features']


class SubscriptionSerializer(serializers.ModelSerializer):
    plan = SubscriptionPlanSerializer(read_only=True)
    user = serializers.StringRelatedField()

    class Meta:
        model = Subscription
        fields = ['id', 'user', 'plan', 'status', 'current_period_start',
                 'current_period_end', 'trial_end', 'created_at']


class InvoiceSerializer(serializers.ModelSerializer):
    subscription = serializers.StringRelatedField()

    class Meta:
        model = Invoice
        fields = ['id', 'subscription', 'amount_due', 'amount_paid',
                 'status', 'due_date', 'paid_at', 'created_at']


class UsageMetricSerializer(serializers.ModelSerializer):
    subscription = serializers.StringRelatedField()

    class Meta:
        model = UsageMetric
        fields = ['id', 'subscription', 'metric_type', 'value', 'date']