import django_filters
from .models import User


class UsersFilter(django_filters.FilterSet):
    first_name = django_filters.CharFilter(method='filter_by_first_name')
    last_name = django_filters.CharFilter(method='filter_by_last_name')
    email = django_filters.CharFilter(method='filter_by_last_email')

    def filter_by_first_name(self, queryset, name, value):
        return queryset.filter(first_name__icontains=value)

    def filter_by_last_name(self, queryset, name, value):
        return queryset.filter(first_name__icontains=value)

    def filter_by_email(self, queryset, name, value):
        return queryset.filter(first_name__icontains=value)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
