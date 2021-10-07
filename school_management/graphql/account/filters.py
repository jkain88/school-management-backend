import django_filters

from ..core.types import FilterInputObjectType
from ...account.models import User


class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name"
        ]


class UserFilterInput(FilterInputObjectType):
    class Meta:
        filterset_class = UserFilter
