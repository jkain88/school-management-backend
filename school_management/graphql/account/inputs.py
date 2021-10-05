import graphene

from .enums import Role


class AccountRegisterInput(graphene.InputObjectType):
    email = graphene.String(required=True)
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    password = graphene.String(required=True)
    age = graphene.Int(required=True)
    role = graphene.Enum.from_enum(Role)(required=True)
    contact_number = graphene.String(required=True)
