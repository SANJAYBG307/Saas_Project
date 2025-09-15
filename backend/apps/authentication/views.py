from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import uuid
from datetime import timedelta
from django.utils import timezone
from .models import EmailVerification, PasswordReset
from .serializers import UserRegistrationSerializer, UserLoginSerializer


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def register(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()

        # Create email verification token
        token = str(uuid.uuid4())
        EmailVerification.objects.create(
            user=user,
            token=token,
            expires_at=timezone.now() + timedelta(hours=24)
        )

        # Send verification email (in production, use proper email service)
        try:
            send_mail(
                'Verify Your Email - CloudFlow',
                f'Click this link to verify your email: http://localhost:8000/api/auth/verify-email/{token}/',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
        except:
            pass  # Email sending failed, but user is still created

        # Generate JWT tokens
        refresh = RefreshToken.for_user(user)

        return Response({
            'message': 'User created successfully. Please check your email for verification.',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
            },
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        }, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

            return Response({
                'message': 'Login successful',
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                },
                'tokens': {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }
            })

        return Response({
            'error': 'Invalid credentials'
        }, status=status.HTTP_401_UNAUTHORIZED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def verify_email(request, token):
    try:
        verification = EmailVerification.objects.get(token=token)
        if verification.is_expired():
            return Response({
                'error': 'Verification token has expired'
            }, status=status.HTTP_400_BAD_REQUEST)

        if not verification.is_verified:
            verification.is_verified = True
            verification.save()

            # You could redirect to a success page here
            return Response({
                'message': 'Email verified successfully!'
            })
        else:
            return Response({
                'message': 'Email already verified'
            })

    except EmailVerification.DoesNotExist:
        return Response({
            'error': 'Invalid verification token'
        }, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def forgot_password(request):
    email = request.data.get('email')
    if not email:
        return Response({
            'error': 'Email is required'
        }, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.get(email=email)
        token = str(uuid.uuid4())

        PasswordReset.objects.create(
            user=user,
            token=token,
            expires_at=timezone.now() + timedelta(hours=1)
        )

        # Send password reset email
        try:
            send_mail(
                'Password Reset - CloudFlow',
                f'Click this link to reset your password: http://localhost:8000/api/auth/reset-password/{token}/',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
        except:
            pass

        return Response({
            'message': 'Password reset link sent to your email'
        })

    except User.DoesNotExist:
        return Response({
            'message': 'If the email exists, a reset link has been sent'
        })


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def reset_password(request, token):
    try:
        reset = PasswordReset.objects.get(token=token)
        if reset.is_expired() or reset.is_used:
            return Response({
                'error': 'Reset token is invalid or expired'
            }, status=status.HTTP_400_BAD_REQUEST)

        new_password = request.data.get('password')
        if not new_password or len(new_password) < 8:
            return Response({
                'error': 'Password must be at least 8 characters long'
            }, status=status.HTTP_400_BAD_REQUEST)

        user = reset.user
        user.set_password(new_password)
        user.save()

        reset.is_used = True
        reset.save()

        return Response({
            'message': 'Password reset successful'
        })

    except PasswordReset.DoesNotExist:
        return Response({
            'error': 'Invalid reset token'
        }, status=status.HTTP_400_BAD_REQUEST)