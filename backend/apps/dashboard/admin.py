from django.contrib import admin
from .models import Project, ProjectMember, Task, Comment, DashboardWidget


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'is_archived', 'created_at']
    list_filter = ['is_archived', 'created_at']
    search_fields = ['name', 'description', 'owner__username']


@admin.register(ProjectMember)
class ProjectMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'project', 'role', 'created_at']
    list_filter = ['role', 'created_at']
    search_fields = ['user__username', 'project__name']


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['title', 'project', 'assignee', 'priority', 'status', 'due_date']
    list_filter = ['priority', 'status', 'created_at']
    search_fields = ['title', 'description', 'project__name']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['task', 'author', 'created_at']
    list_filter = ['created_at']
    search_fields = ['content', 'task__title', 'author__username']


@admin.register(DashboardWidget)
class DashboardWidgetAdmin(admin.ModelAdmin):
    list_display = ['user', 'widget_type', 'title', 'position_x', 'position_y']
    list_filter = ['widget_type', 'created_at']
    search_fields = ['title', 'user__username']