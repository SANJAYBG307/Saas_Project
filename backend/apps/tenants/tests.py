from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import Client, Domain


class TenantModelTests(TestCase):
    """Test cases for tenant models"""

    def setUp(self):
        self.client_data = {
            'schema_name': 'test_tenant',
            'name': 'Test Tenant Company',
            'created_on_domain': 'test.example.com'
        }

    def test_client_creation(self):
        """Test client (tenant) creation"""
        client = Client.objects.create(**self.client_data)
        self.assertEqual(client.schema_name, 'test_tenant')
        self.assertEqual(client.name, 'Test Tenant Company')

    def test_domain_creation(self):
        """Test domain creation for tenant"""
        client = Client.objects.create(**self.client_data)
        domain = Domain.objects.create(
            domain='test.example.com',
            tenant=client,
            is_primary=True
        )
        self.assertEqual(domain.domain, 'test.example.com')
        self.assertEqual(domain.tenant, client)
        self.assertTrue(domain.is_primary)

    def test_client_string_representation(self):
        """Test client string representation"""
        client = Client.objects.create(**self.client_data)
        self.assertEqual(str(client), 'Test Tenant Company')


class TenantViewTests(APITestCase):
    """Test cases for tenant views"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword123'
        )
        self.client_data = {
            'schema_name': 'test_tenant',
            'name': 'Test Tenant Company',
            'created_on_domain': 'test.example.com'
        }

    def test_tenant_creation_authenticated(self):
        """Test tenant creation when authenticated"""
        self.client.force_authenticate(user=self.user)
        url = reverse('tenants:create-tenant')
        response = self.client.post(url, self.client_data)
        # Add appropriate status code check based on your implementation
        self.assertIn(response.status_code, [status.HTTP_201_CREATED, status.HTTP_200_OK])

    def test_tenant_list(self):
        """Test tenant listing"""
        self.client.force_authenticate(user=self.user)
        url = reverse('tenants:tenant-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)