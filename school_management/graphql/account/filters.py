import django_filters

from ..core.types import FilterInputObjectType
from ..core.filters import EnumFilter
from ...account.models import Student
from .enums import Role

def filter_by_role(qs, _, value):
    qs = qs.filter(role=value)
    return qs


class StudentFilter(django_filters.FilterSet):
    role = EnumFilter(input_class=Role, method=filter_by_role)
    email = django_filters.CharFilter(lookup_expr='icontains')
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')


    class Meta:
        model = Student
        fields = [
            "email",
            "first_name",
            "last_name",
            "role"
        ]


class StudentFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = StudentFilter
