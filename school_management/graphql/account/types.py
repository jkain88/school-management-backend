from graphene_django import DjangoObjectType

from ...account.models import User

class User(DjangoObjectType):
    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "age",
            "role"
        )