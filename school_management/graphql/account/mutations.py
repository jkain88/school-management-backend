import graphene
from graphql_jwt import ObtainJSONWebToken, Verify
from graphql_jwt.exceptions import JSONWebTokenError

from .types import User
from ..core.types import Error

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
            result = super().mutate(root, info, **kwargs)
        except JSONWebTokenError as e:
            return CreateToken(errors=[Error(message=str(e))])
        else:
            return result

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user, errors=[])
