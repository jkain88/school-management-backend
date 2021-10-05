import graphene
from graphql_jwt import ObtainJSONWebToken, Verify
from graphql_jwt.exceptions import JSONWebTokenError

from .inputs import (
    AccountRegisterInput,
    AddressCreateInput
)
from .types import (
    User,
    Address
)
from ..core.mutations import ModelMutation
from ..core.types import Error
from ...account import models


class CreateToken(ObtainJSONWebToken):
    """Mutation that authenticates a user and returns token and user data.

    It overrides the default graphql_jwt.ObtainJSONWebToken to wrap potential
    authentication errors in our Error type, which is consistent to how the rest of
    the mutation works.
    """

    errors = graphene.List(Error, required=True)
    user = graphene.Field(User)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        try:
            return super().mutate(root, info, **kwargs)
        except JSONWebTokenError:
            return None

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user, errors=[])


class AccountRegister(ModelMutation):
    user = graphene.Field(User)

    class Arguments:
        input = AccountRegisterInput(description="Fields required to create a user.", required=True)

    class Meta:
        description = "Registers a new user."
        exclude = ["password"]
        model = models.User

    @classmethod
    def perform_mutation(cls, _root, info, **data):
        data = data.get("input")
        password = data.pop("password")

        user = models.User.objects.create(**data)
        user.set_password(password)
        user.save()

        return AccountRegister(user=user)


class AddressCreate(ModelMutation):
    address = graphene.Field(Address)

    class Arguments:
        input = AddressCreateInput(description="Fields required to create an address for a user", required=True)

    class Meta:
        description = "Creates an address for a user"
        model = models.Address

    @classmethod
    def perform_mutation(cls, _root, info, **data):
        data = data.get("input")
        user_id = data.pop("user")
        user = cls.get_node_or_error(info, user_id, User)

        address = models.Address.objects.create(**data, user=user)
        print(data)
        print(user)

        return AddressCreate(address=address)