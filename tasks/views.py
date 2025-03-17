import concurrent.futures
from django.contrib.auth.models import User
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .filters import TaskFilter
from .models import Task
from .serializers import UserSerializer, TaskSerializer


class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter 

    def get_queryset(self):
        return Task.objects.filter(assigned_to=self.request.user)


class ReportGenerationView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future1 = executor.submit(self._count_completed_tasks)
            future2 = executor.submit(self._count_pending_tasks)
            future3 = executor.submit(self._categorize_by_priority)

            completed_tasks = future1.result()
            pending_tasks = future2.result()
            categorized_tasks = future3.result()

        report = {
            "completed_tasks": completed_tasks,
            "pending_tasks": pending_tasks,
            "tasks_by_priority": categorized_tasks
        }

        return Response(report, status=status.HTTP_200_OK)

    def _count_completed_tasks(self):
        """Count the number of completed tasks"""
        return Task.objects.filter(status='Completed').count()

    def _count_pending_tasks(self):
        """Count the number of pending tasks"""
        return Task.objects.filter(status='Pending').count()

    def _categorize_by_priority(self):
        """Categorize tasks by priority"""
        tasks = Task.objects.values('priority').annotate(count=Count('priority')).order_by('priority')
        return {task['priority']: task['count'] for task in tasks}
