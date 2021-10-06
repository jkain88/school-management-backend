import graphene
from graphql_jwt.decorators import login_required

from .mutations import (
    AccountRegister,
    AccountUpdate,
    AccountDelete,
    AddressCreate,
    AddressUpdate,
    AddressDelete,
    CreateToken
)
from .types import User
from ..core.fields import FilterInputConnectionField


class AccountQueries(graphene.ObjectType):
    me = graphene.Field(User, description="Return authenticated user instance")

    @login_required
    def resolve_me(self, info):
        return info.context.user


class AccountMutations(graphene.ObjectType):
    account_register = AccountRegister.Field()
    account_update = AccountUpdate.Field()
    account_delete = AccountDelete.Field()

    address_create = AddressCreate.Field()
    address_update = AddressUpdate.Field()
    address_delete = AddressDelete.Field()

    create_token = CreateToken.Field()
