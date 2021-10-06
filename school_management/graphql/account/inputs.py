import graphene

from .enums import (
    Role,
    AddressType
)


class AccountInput(graphene.InputObjectType):
    email = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    password = graphene.String()
    age = graphene.Int()
    role = graphene.Enum.from_enum(Role)()
    contact_number = graphene.String()


class AddressInput(graphene.InputObjectType):
    street = graphene.String()
    city_area = graphene.String()
    city = graphene.String()
    province = graphene.String()
    postal_code = graphene.String()
    user = graphene.ID(description="User ID")
    address_type = graphene.Enum.from_enum(AddressType)()
