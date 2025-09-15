from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta
from .models import Project, ProjectMember, Task, Comment, DashboardWidget
from .serializers import (
    ProjectSerializer,
    ProjectMemberSerializer,
    TaskSerializer,
    CommentSerializer,
    DashboardWidgetSerializer
)


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(
            Q(owner=self.request.user) | Q(members=self.request.user)
        ).distinct()

    def perform_create(self, serializer):
        project = serializer.save(owner=self.request.user)
        ProjectMember.objects.create(
            project=project,
            user=self.request.user,
            role='owner'
        )

    @action(detail=True, methods=['post'])
    def add_member(self, request, pk=None):
        project = self.get_object()
        user_id = request.data.get('user_id')
        role = request.data.get('role', 'member')

        if not user_id:
            return Response({'error': 'User ID is required'},
                          status=status.HTTP_400_BAD_REQUEST)

        try:
            from django.contrib.auth.models import User
            user = User.objects.get(id=user_id)

            member, created = ProjectMember.objects.get_or_create(
                project=project,
                user=user,
                defaults={'role': role}
            )

            if not created:
                member.role = role
                member.save()

            serializer = ProjectMemberSerializer(member)
            return Response(serializer.data)

        except User.DoesNotExist:
            return Response({'error': 'User not found'},
                          status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['get'])
    def statistics(self, request, pk=None):
        project = self.get_object()
        stats = {
            'total_tasks': project.tasks.count(),
            'completed_tasks': project.tasks.filter(status='done').count(),
            'in_progress_tasks': project.tasks.filter(status='in_progress').count(),
            'overdue_tasks': project.tasks.filter(
                due_date__lt=timezone.now(),
                status__in=['todo', 'in_progress']
            ).count(),
            'members_count': project.members.count(),
        }
        return Response(stats)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_projects = Project.objects.filter(
            Q(owner=self.request.user) | Q(members=self.request.user)
        )
        return Task.objects.filter(project__in=user_projects)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    @action(detail=False, methods=['get'])
    def my_tasks(self, request):
        tasks = self.get_queryset().filter(assignee=request.user)
        serializer = self.get_serializer(tasks, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def overdue(self, request):
        overdue_tasks = self.get_queryset().filter(
            due_date__lt=timezone.now(),
            status__in=['todo', 'in_progress']
        )
        serializer = self.get_serializer(overdue_tasks, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user_projects = Project.objects.filter(
            Q(owner=self.request.user) | Q(members=self.request.user)
        )
        return Comment.objects.filter(task__project__in=user_projects)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class DashboardWidgetViewSet(viewsets.ModelViewSet):
    serializer_class = DashboardWidgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DashboardWidget.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=False, methods=['get'])
    def dashboard_data(self, request):
        # Get dashboard statistics for the user
        user_projects = Project.objects.filter(
            Q(owner=request.user) | Q(members=request.user)
        ).distinct()

        user_tasks = Task.objects.filter(project__in=user_projects)
        assigned_tasks = user_tasks.filter(assignee=request.user)

        # Recent activity (last 7 days)
        last_week = timezone.now() - timedelta(days=7)
        recent_tasks = user_tasks.filter(created_at__gte=last_week)
        recent_comments = Comment.objects.filter(
            task__project__in=user_projects,
            created_at__gte=last_week
        )

        data = {
            'projects': {
                'total': user_projects.count(),
                'active': user_projects.filter(is_archived=False).count(),
            },
            'tasks': {
                'total': assigned_tasks.count(),
                'completed': assigned_tasks.filter(status='done').count(),
                'in_progress': assigned_tasks.filter(status='in_progress').count(),
                'overdue': assigned_tasks.filter(
                    due_date__lt=timezone.now(),
                    status__in=['todo', 'in_progress']
                ).count(),
            },
            'recent_activity': {
                'new_tasks': recent_tasks.count(),
                'new_comments': recent_comments.count(),
            },
            'task_distribution': list(
                user_tasks.values('status').annotate(count=Count('status'))
            )
        }

        return Response(data)