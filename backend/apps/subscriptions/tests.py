from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Plan, Subscription
from decimal import Decimal


class SubscriptionModelTests(TestCase):
    """Test cases for subscription models"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.plan = Plan.objects.create(
            name='Basic Plan',
            price=Decimal('9.99'),
            billing_cycle='monthly',
            features={'storage': '10GB', 'users': 5}
        )

    def test_plan_creation(self):
        """Test plan creation"""
        self.assertEqual(self.plan.name, 'Basic Plan')
        self.assertEqual(self.plan.price, Decimal('9.99'))
        self.assertEqual(self.plan.billing_cycle, 'monthly')

    def test_subscription_creation(self):
        """Test subscription creation"""
        subscription = Subscription.objects.create(
            user=self.user,
            plan=self.plan,
            status='active'
        )
        self.assertEqual(subscription.user, self.user)
        self.assertEqual(subscription.plan, self.plan)
        self.assertEqual(subscription.status, 'active')

    def test_plan_string_representation(self):
        """Test plan string representation"""
        self.assertEqual(str(self.plan), 'Basic Plan')


class SubscriptionViewTests(APITestCase):
    """Test cases for subscription views"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.plan = Plan.objects.create(
            name='Basic Plan',
            price=Decimal('9.99'),
            billing_cycle='monthly',
            features={'storage': '10GB'}
        )

    def test_get_plans(self):
        """Test getting available plans"""
        url = reverse('subscriptions:plans')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_subscription_authenticated(self):
        """Test creating subscription when authenticated"""
        self.client.force_authenticate(user=self.user)
        url = reverse('subscriptions:subscribe')
        data = {'plan_id': self.plan.id}
        response = self.client.post(url, data)
        # Add appropriate status code check based on your implementation
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])

    def test_create_subscription_unauthenticated(self):
        """Test creating subscription when not authenticated"""
        url = reverse('subscriptions:subscribe')
        data = {'plan_id': self.plan.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)