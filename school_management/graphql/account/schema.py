import graphene
from graphql_jwt.decorators import login_required
import graphene_django_optimizer as gql_optimizer

from .mutations import (
    AccountCreate,
    AccountUpdate,
    AccountDelete,
    AddressCreate,
    AddressUpdate,
    AddressDelete,
    CreateToken,
)
from .types import User
from .filters import UserFilterInput
from ..core.fields import FilterInputConnectionField
from ..core.types import FilterInputObjectType
from ...account import models


class AccountQueries(graphene.ObjectType):
    #me = graphene.Field(User, description="Return authenticated user instance")
    users = FilterInputConnectionField(
        User,
        filter=UserFilterInput(description="Filtering options for users."),
        description="List of users"
    )
    students = FilterInputConnectionField(
        User,
        filter=UserFilterInput(description="Filtering options for users."),
        description="List of users"
    )

    @login_required
    def resolve_me(self, info):
        return info.context.user

    def resolve_users(self, info, **_kwargs):
        qs = models.User.objects.all()
        qs = qs.order_by("id")

        return gql_optimizer.query(qs, info)

    def resolve_students(self, info, **_kwargs):
        qs = models.User.objects.all().filter(role="student")
        qs = qs.order_by("id")

        return gql_optimizer.query(qs, info)


class AccountMutations(graphene.ObjectType):
    account_create = AccountCreate.Field()
    account_update = AccountUpdate.Field()
    account_delete = AccountDelete.Field()

    address_create = AddressCreate.Field()
    address_update = AddressUpdate.Field()
    address_delete = AddressDelete.Field()

    create_token = CreateToken.Field()
