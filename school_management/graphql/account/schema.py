import graphene

from .mutations import CreateToken
from .types import User

class AccountQueries(graphene.ObjectType):
    me = graphene.Field(User, description="Return authenticated user instance")

class AccountMutations(graphene.ObjectType):
    create_token = CreateToken.Field()
