from django.contrib import admin
from .models import UserProfile, Activity


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company', 'position', 'created_at']
    search_fields = ['user__username', 'company', 'position']
    list_filter = ['company', 'created_at']


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'created_at']
    search_fields = ['user__username', 'action', 'description']
    list_filter = ['action', 'created_at']
    readonly_fields = ['created_at']