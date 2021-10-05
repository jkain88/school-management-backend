from graphene import relay
from graphene_django import DjangoObjectType

from ...account.models import User


class User(DjangoObjectType):
    class Meta:
        interfaces = [relay.Node]
        model = User
        fields = (
            "id",
            "email",
            "first_name",
            "last_name",
            "age",
            "role"
        )
