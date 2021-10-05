import graphene

from .mutations import (
    AccountRegister,
    AddressCreate,
    CreateToken
)
from .types import User


class AccountQueries(graphene.ObjectType):
    me = graphene.Field(User, description="Return authenticated user instance")


class AccountMutations(graphene.ObjectType):
    account_register = AccountRegister.Field()
    address_create = AddressCreate.Field()
    create_token = CreateToken.Field()

