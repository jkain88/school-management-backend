import django_filters

from ..core.types import FilterInputObjectType
from ..core.filters import EnumFilter
from ...account.models import User
from .enums import Role

def filter_by_role(qs, _, value):
    qs = qs.filter(role=value)
    return qs


class UserFilter(django_filters.FilterSet):
    role = EnumFilter(input_class=Role, method=filter_by_role)
    email = django_filters.CharFilter(lookup_expr='icontains')
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')


    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "role"
        ]


class UserFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = UserFilter
