from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, ActivityViewSet

router = DefaultRouter()
router.register(r'profiles', UserProfileViewSet)
router.register(r'activities', ActivityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]