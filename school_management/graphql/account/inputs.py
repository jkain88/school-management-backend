import graphene

from .enums import (
    Role,
    AddressType
)


class AccountRegisterInput(graphene.InputObjectType):
    email = graphene.String(required=True)
    first_name = graphene.String(required=True)
    last_name = graphene.String(required=True)
    password = graphene.String(required=True)
    age = graphene.Int(required=True)
    role = graphene.Enum.from_enum(Role)(required=True)
    contact_number = graphene.String(required=True)


class AddressCreateInput(graphene.InputObjectType):
    street = graphene.String(required=True)
    city_area = graphene.String(required=True)
    city = graphene.String(required=True)
    province = graphene.String(required=True)
    postal_code = graphene.String(required=True)
    user = graphene.ID(required=True, description="User ID")
    address_type = graphene.Enum.from_enum(AddressType)(required=True)
