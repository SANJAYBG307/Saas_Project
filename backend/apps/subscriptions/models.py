from django.db import models
from django.contrib.auth.models import User
from apps.core.models import BaseModel
from decimal import Decimal


class SubscriptionPlan(BaseModel):
    PLAN_TYPES = [
        ('starter', 'Starter'),
        ('professional', 'Professional'),
        ('enterprise', 'Enterprise'),
    ]

    name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPES)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    billing_period = models.CharField(max_length=20, default='monthly')  # monthly, yearly
    max_users = models.IntegerField()
    max_storage_gb = models.IntegerField()
    features = models.JSONField(default=list)
    stripe_price_id = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.name} - ${self.price}/{self.billing_period}"


class Subscription(BaseModel):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('canceled', 'Canceled'),
        ('past_due', 'Past Due'),
        ('unpaid', 'Unpaid'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscriptions')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    stripe_subscription_id = models.CharField(max_length=100, blank=True)
    current_period_start = models.DateTimeField()
    current_period_end = models.DateTimeField()
    trial_end = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.plan.name} ({self.status})"


class Invoice(BaseModel):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('paid', 'Paid'),
        ('void', 'Void'),
        ('uncollectible', 'Uncollectible'),
    ]

    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='invoices')
    stripe_invoice_id = models.CharField(max_length=100, blank=True)
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    due_date = models.DateTimeField()
    paid_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Invoice {self.id} - ${self.amount_due} ({self.status})"


class UsageMetric(BaseModel):
    METRIC_TYPES = [
        ('api_calls', 'API Calls'),
        ('storage_used', 'Storage Used (GB)'),
        ('users_active', 'Active Users'),
        ('bandwidth', 'Bandwidth (GB)'),
    ]

    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='usage_metrics')
    metric_type = models.CharField(max_length=50, choices=METRIC_TYPES)
    value = models.DecimalField(max_digits=15, decimal_places=2)
    date = models.DateField()

    class Meta:
        unique_together = ['subscription', 'metric_type', 'date']
        ordering = ['-date']

    def __str__(self):
        return f"{self.subscription} - {self.metric_type}: {self.value}"