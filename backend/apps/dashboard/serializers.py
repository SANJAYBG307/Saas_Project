from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Project, ProjectMember, Task, Comment, DashboardWidget


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class ProjectMemberSerializer(serializers.ModelSerializer):
    user = UserSimpleSerializer(read_only=True)

    class Meta:
        model = ProjectMember
        fields = ['id', 'user', 'role', 'created_at']


class ProjectSerializer(serializers.ModelSerializer):
    owner = UserSimpleSerializer(read_only=True)
    members_detail = ProjectMemberSerializer(
        source='projectmember_set',
        many=True,
        read_only=True
    )
    tasks_count = serializers.SerializerMethodField()

    class Meta:
        model = Project
        fields = ['id', 'name', 'description', 'owner', 'color',
                 'is_archived', 'created_at', 'members_detail', 'tasks_count']

    def get_tasks_count(self, obj):
        return obj.tasks.count()


class CommentSerializer(serializers.ModelSerializer):
    author = UserSimpleSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at']


class TaskSerializer(serializers.ModelSerializer):
    creator = UserSimpleSerializer(read_only=True)
    assignee = UserSimpleSerializer(read_only=True)
    project = serializers.StringRelatedField()
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'project', 'assignee',
                 'creator', 'priority', 'status', 'due_date', 'completed_at',
                 'created_at', 'comments', 'comments_count']

    def get_comments_count(self, obj):
        return obj.comments.count()


class DashboardWidgetSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = DashboardWidget
        fields = ['id', 'user', 'widget_type', 'title', 'configuration',
                 'position_x', 'position_y', 'width', 'height', 'created_at']