import django_filters
from .models import Task


class TaskFilter(django_filters.FilterSet):
    priority = django_filters.ChoiceFilter(choices=Task.PRIORITY_CHOICES)
    status = django_filters.CharFilter(lookup_expr='icontains')
    due_date = django_filters.DateTimeFilter(lookup_expr='lte')

    class Meta:
        model = Task
        fields = ['priority', 'status', 'due_date']
