import graphene

from .types import User

class AccountQueries(graphene.ObjectType):
    me = graphene.Field(User, description="Return authenticated user instance")
