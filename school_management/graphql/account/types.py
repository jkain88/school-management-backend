import graphene
from graphene import relay
from graphene_django import DjangoObjectType
import graphene_django_optimizer as gql_optimizer

from ...account import models


class Address(DjangoObjectType):
    class Meta:
        interfaces = [relay.Node]
        model = models.Address
        only_fields = [
            "id",
            "street",
            "city_area",
            "city",
            "province",
            "postal_code",
            "address_type"
        ]


class User(DjangoObjectType):
    addresses = gql_optimizer.field(
        graphene.List(Address, description="User's list of addresses")
    )

    class Meta:
        interfaces = [relay.Node]
        model = models.User
        only_fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "age",
            "role"
        ]

    @staticmethod
    def resolve_addresses(root:models.User, _):
        return root.addresses.all()
