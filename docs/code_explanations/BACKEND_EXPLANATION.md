# Backend Code Explanation (Django)

## Django Settings Configuration (`backend/saas_platform/settings.py`)

### Line-by-Line Breakdown:

**Lines 1-10: Imports and Base Setup**
```python
from pathlib import Path
import os
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent
```
- `from pathlib import Path`: Modern way to handle file paths
- `from decouple import config`: Safely loads environment variables
- `BASE_DIR`: Gets the main project directory path
- `__file__.resolve().parent.parent`: Goes up 2 directories from settings.py

**Lines 12-18: Security Settings**
```python
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production')
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = ['localhost', '127.0.0.1', '.ngrok.io', '.herokuapp.com']
```
- `SECRET_KEY`: Used for cryptographic operations (passwords, sessions)
- `config('SECRET_KEY', default=...)`: Gets from .env file or uses default
- `DEBUG = True`: Shows detailed error messages (only for development)
- `ALLOWED_HOSTS`: Websites allowed to serve this application

**Lines 20-35: Application Configuration**
```python
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'django_tenants',
]

LOCAL_APPS = [
    'apps.core',
    'apps.tenants',
    'apps.authentication',
    'apps.subscriptions',
    'apps.dashboard',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS
```
- `DJANGO_APPS`: Built-in Django applications
- `THIRD_PARTY_APPS`: External packages we installed
- `LOCAL_APPS`: Our custom applications
- Each app provides specific functionality (auth, subscriptions, etc.)

**Lines 37-50: Middleware Configuration**
```python
MIDDLEWARE = [
    'django_tenants.middleware.main.TenantMainMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```
- Middleware processes every request/response
- `TenantMainMiddleware`: Handles multi-tenant routing
- `CorsMiddleware`: Allows frontend to communicate with backend
- `SecurityMiddleware`: Basic security protections
- Order matters - each processes requests in this sequence

**Lines 70-85: Database Configuration**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django_tenants.postgresql_backend',
        'NAME': config('DB_NAME', default='saas_platform'),
        'USER': config('DB_USER', default='root'),
        'PASSWORD': config('DB_PASSWORD', default='password'),
        'HOST': config('DB_HOST', default='localhost'),
        'PORT': config('DB_PORT', default='3306'),
    }
}
```
- `DATABASES`: Configuration for database connection
- `ENGINE`: Database type (PostgreSQL with tenant support)
- Gets connection details from environment variables
- Falls back to defaults if .env file doesn't exist

**Lines 87-95: Multi-Tenant Configuration**
```python
TENANT_MODEL = "tenants.Client"
TENANT_DOMAIN_MODEL = "tenants.Domain"

SHARED_APPS = (
    'django_tenants',
    'apps.tenants',
    'django.contrib.auth',
    'django.contrib.admin',
)

TENANT_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'apps.core',
    'apps.authentication',
    'apps.subscriptions',
    'apps.dashboard',
)
```
- `TENANT_MODEL`: Model that represents each company/tenant
- `SHARED_APPS`: Applications shared across all tenants
- `TENANT_APPS`: Applications with separate data per tenant
- Each tenant gets their own database schema

**Lines 130-145: API Configuration**
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20
}
```
- `JWTAuthentication`: Uses JSON Web Tokens for API security
- `IsAuthenticated`: Requires login for API access
- `PageNumberPagination`: Splits large data into pages (20 items per page)

**Lines 147-155: JWT Token Configuration**
```python
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}
```
- `ACCESS_TOKEN_LIFETIME`: How long login tokens last (1 hour)
- `REFRESH_TOKEN_LIFETIME`: How long refresh tokens last (7 days)
- `ROTATE_REFRESH_TOKENS`: Creates new tokens on refresh
- Security feature to prevent token theft

---

## URL Routing (`backend/saas_platform/urls.py`)

### Line-by-Line Breakdown:

**Lines 1-10: Imports**
```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
```
- `path, include`: Functions for URL routing
- `static`: Serves uploaded files in development
- `TemplateView`: Renders HTML templates

**Lines 12-20: URL Patterns**
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.authentication.urls')),
    path('api/subscriptions/', include('apps.subscriptions.urls')),
    path('api/dashboard/', include('apps.dashboard.urls')),
    path('api/core/', include('apps.core.urls')),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('dashboard/', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
]
```
- `path('admin/')`: Django admin interface at /admin/
- `path('api/auth/')`: All authentication URLs start with /api/auth/
- `include('apps.authentication.urls')`: Loads URLs from authentication app
- `path('')`: Root URL (/) shows landing page
- `TemplateView.as_view()`: Renders HTML template

**Lines 22-25: Static Files in Development**
```python
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```
- Only runs in development (DEBUG=True)
- Serves uploaded files and CSS/JS files
- In production, web server handles static files

---

## Database Models (`backend/apps/core/models.py`)

### Line-by-Line Breakdown:

**Lines 1-10: Base Model**
```python
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
```
- `from django.db import models`: Import Django database tools
- `BaseModel`: Parent class for other models
- `auto_now_add=True`: Sets timestamp when record is created
- `auto_now=True`: Updates timestamp when record is modified
- `abstract = True`: This model won't create a database table

**Lines 12-25: User Profile Model**
```python
class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone_number = models.CharField(max_length=20, blank=True)
    company = models.CharField(max_length=100, blank=True)
    position = models.CharField(max_length=100, blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    timezone = models.CharField(max_length=50, default='UTC')

    def __str__(self):
        return f"{self.user.username}'s Profile"
```
- `OneToOneField`: Each user has exactly one profile
- `on_delete=models.CASCADE`: Delete profile when user is deleted
- `CharField`: Text field with maximum length
- `ImageField`: Stores profile pictures in 'avatars/' folder
- `__str__()`: How this object appears when printed

**Lines 27-40: Activity Tracking Model**
```python
class Activity(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='activities')
    action = models.CharField(max_length=100)
    description = models.TextField()
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Activities'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.action}"
```
- `ForeignKey`: Links to User (one user can have many activities)
- `TextField`: Long text without length limit
- `GenericIPAddressField`: Stores IPv4 or IPv6 addresses
- `ordering = ['-created_at']`: Shows newest activities first
- `verbose_name_plural`: How it appears in admin panel

---

## API Views (`backend/apps/authentication/views.py`)

### Line-by-Line Breakdown:

**Lines 1-15: Imports**
```python
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
```
- `rest_framework`: API development framework
- `status`: HTTP status codes (200, 404, 500, etc.)
- `permissions`: Controls who can access endpoints
- `RefreshToken`: Creates JWT tokens for authentication

**Lines 17-25: Registration Endpoint**
```python
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
```
- `@api_view(['POST'])`: Only accepts POST requests
- `@permission_classes([permissions.AllowAny])`: No login required
- `serializer`: Validates and processes form data
- `serializer.is_valid()`: Checks if data is correct
- `serializer.save()`: Creates new user in database

**Lines 30-45: Email Verification**
```python
        token = str(uuid.uuid4())
        EmailVerification.objects.create(
            user=user,
            token=token,
            expires_at=timezone.now() + timedelta(hours=24)
        )

        send_mail(
            'Verify Your Email - CloudFlow',
            f'Click this link to verify: http://localhost:8000/api/auth/verify-email/{token}/',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
```
- `uuid.uuid4()`: Creates unique random token
- `EmailVerification.objects.create()`: Saves verification record
- `timedelta(hours=24)`: Token expires in 24 hours
- `send_mail()`: Sends email with verification link
- `fail_silently=False`: Raise error if email fails

**Lines 50-70: JWT Token Generation**
```python
        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'User created successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)
```
- `RefreshToken.for_user()`: Creates tokens for this user
- `Response()`: Sends JSON response to frontend
- Returns user info and both access/refresh tokens
- `status.HTTP_201_CREATED`: HTTP 201 status (resource created)

**Lines 75-95: Login Endpoint**
```python
@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def login(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({...})

        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)
```
- Takes username and password from request
- `authenticate()`: Django function to verify credentials
- If valid, creates tokens and returns user info
- If invalid, returns 401 Unauthorized error

---

## Serializers (`backend/apps/authentication/serializers.py`)

### Line-by-Line Breakdown:

**Lines 1-10: User Registration Serializer**
```python
from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True)
```
- `serializers.ModelSerializer`: Automatically creates form fields from model
- `write_only=True`: Field not included in API responses (security)
- `validate_password`: Django's built-in password strength checker

**Lines 12-20: Field Configuration**
```python
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password_confirm']

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError("Passwords don't match")
        return attrs
```
- `Meta.model = User`: This serializer works with User model
- `fields`: Which fields to include in the form
- `validate()`: Custom validation logic
- Checks that both password fields match

**Lines 22-26: Create User Method**
```python
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user
```
- `validated_data.pop()`: Removes password_confirm (not needed for creation)
- `create_user()`: Django method that properly hashes password
- `**validated_data`: Spreads dictionary as function arguments

This backend code creates a secure, multi-tenant SaaS platform with user authentication, subscription management, project tracking, and a full API for the frontend to interact with.