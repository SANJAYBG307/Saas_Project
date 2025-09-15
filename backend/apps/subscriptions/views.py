from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.conf import settings
import stripe
from .models import SubscriptionPlan, Subscription, Invoice, UsageMetric
from .serializers import (
    SubscriptionPlanSerializer,
    SubscriptionSerializer,
    InvoiceSerializer,
    UsageMetricSerializer
)

stripe.api_key = settings.STRIPE_SECRET_KEY


class SubscriptionPlanViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SubscriptionPlan.objects.filter(is_active=True)
    serializer_class = SubscriptionPlanSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured_plan = self.queryset.filter(plan_type='professional').first()
        if featured_plan:
            serializer = self.get_serializer(featured_plan)
            return Response(serializer.data)
        return Response({'message': 'No featured plan found'})


class SubscriptionViewSet(viewsets.ModelViewSet):
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Subscription.objects.filter(user=self.request.user)

    @action(detail=False, methods=['get'])
    def current(self, request):
        subscription = self.get_queryset().filter(status='active').first()
        if subscription:
            serializer = self.get_serializer(subscription)
            return Response(serializer.data)
        return Response({'message': 'No active subscription found'},
                       status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def create_subscription(self, request):
        plan_id = request.data.get('plan_id')
        if not plan_id:
            return Response({'error': 'Plan ID is required'},
                          status=status.HTTP_400_BAD_REQUEST)

        try:
            plan = SubscriptionPlan.objects.get(id=plan_id)
        except SubscriptionPlan.DoesNotExist:
            return Response({'error': 'Plan not found'},
                          status=status.HTTP_404_NOT_FOUND)

        # Create Stripe customer if doesn't exist
        customer = None
        try:
            # In a real app, you'd store the Stripe customer ID on the user model
            customer = stripe.Customer.create(
                email=request.user.email,
                name=f"{request.user.first_name} {request.user.last_name}",
            )
        except stripe.error.StripeError as e:
            return Response({'error': str(e)},
                          status=status.HTTP_400_BAD_REQUEST)

        # Create subscription in Stripe
        try:
            stripe_subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[{'price': plan.stripe_price_id}],
            )

            # Create subscription in our database
            subscription = Subscription.objects.create(
                user=request.user,
                plan=plan,
                stripe_subscription_id=stripe_subscription.id,
                current_period_start=stripe_subscription.current_period_start,
                current_period_end=stripe_subscription.current_period_end,
                status='active'
            )

            serializer = self.get_serializer(subscription)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except stripe.error.StripeError as e:
            return Response({'error': str(e)},
                          status=status.HTTP_400_BAD_REQUEST)


class InvoiceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = InvoiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Invoice.objects.filter(subscription__user=self.request.user)


class UsageMetricViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UsageMetricSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return UsageMetric.objects.filter(subscription__user=self.request.user)

    @action(detail=False, methods=['get'])
    def current_month(self, request):
        from datetime import datetime
        current_month = datetime.now().month
        current_year = datetime.now().year

        metrics = self.get_queryset().filter(
            date__month=current_month,
            date__year=current_year
        )
        serializer = self.get_serializer(metrics, many=True)
        return Response(serializer.data)