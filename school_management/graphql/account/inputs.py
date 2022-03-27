import graphene

from .enums import (
    Role,
    AddressType
)


class UserInput(graphene.InputObjectType):
    email = graphene.String()
    first_name = graphene.String()
    last_name = graphene.String()
    password = graphene.String()
    age = graphene.Int()
    contact_number = graphene.String()
    role = Role()


class StudentInput(graphene.InputObjectType):
    mother_name = graphene.String()
    father_name = graphene.String()


class AddressInput(graphene.InputObjectType):
    street = graphene.String()
    city_area = graphene.String()
    city = graphene.String()
    province = graphene.String()
    postal_code = graphene.String()
    user = graphene.ID(description="User ID")
    address_type = AddressType()
