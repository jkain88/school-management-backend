import graphene
from graphql_jwt import ObtainJSONWebToken, Verify
from graphql_jwt.exceptions import JSONWebTokenError

from .inputs import (
    StudentInput,
    AddressInput
)
from .types import (
    Student,
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
    #user = graphene.Field(User)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        try:
            return super().mutate(root, info, **kwargs)
        except JSONWebTokenError:
            return None

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user, errors=[])


class StudentCreate(ModelMutation):
    user = graphene.Field(Student)

    class Arguments:
        input = StudentInput(description="Fields required to create a student.", required=True)

    class Meta:
        description = "Registers a new user."
        exclude = ["password"]
        model = models.Student

    @classmethod
    def perform_mutation(cls, _root, info, **data):
        data = data.get("input")
        password = data.pop("password")

        user = models.Student.objects.create(**data)
        user.set_password(password)
        user.save()
        return StudentCreate(user=user)


class StudentUpdate(ModelMutation):
    user = graphene.Field(Student)

    class Arguments:
        id = graphene.ID(description="Student ID")
        input = StudentInput(description="Fields required to update a student.", required=True)

    class Meta:
        description = "Updates a user."
        exclude = ["password"]
        model = models.Student

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, _root, info, **data):
        user = cls.update_instance(**data)
        return StudentUpdate(user=user)


class StudentDelete(ModelMutation):
    user = graphene.Field(Student)

    class Arguments:
        id = graphene.ID(description="Student ID")

    class Meta:
        description = "Deletes a user"
        exclude = ["password"]
        model = models.Student

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, _root, info, **data):
        user = cls.get_node_or_error(info, data.get("id"))
        user.delete()
        return StudentDelete(user=user)


class AddressCreate(ModelMutation):
    address = graphene.Field(Address)

    class Arguments:
        input = AddressInput(description="Fields required to create an address for a user", required=True)

    class Meta:
        description = "Creates an address for a user"
        model = models.Address

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, _root, info, **data):
        data = data.get("input")
        user_id = data.pop("user")
        user = cls.get_node_or_error(info, user_id, User)

        address = models.Address.objects.create(**data, user=user)
        return AddressCreate(address=address)


class AddressUpdate(ModelMutation):
    address = graphene.Field(Address)

    class Arguments:
        id = graphene.ID(description="Address ID",required=True)
        input = AddressInput(description="Fields required to update an address for a user", required=True)

    class Meta:
        description = "Updates an address"
        model = models.Address

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, _root, info, **data):
        address = cls.update_instance(**data)
        return AddressUpdate(address=address)


class AddressDelete(ModelMutation):
    address = graphene.Field(Address)

    class Arguments:
        id = graphene.ID(description="Address ID",required=True)

    class Meta:
        description = "Deletes an address"
        model = models.Address

    @classmethod
    def check_permissions(cls, context):
        return context.user.is_authenticated

    @classmethod
    def perform_mutation(cls, _root, info, **data):
        address = cls.get_node_or_error(info, data.get("id"))
        address.delete()
        return AddressDelete(address=address)