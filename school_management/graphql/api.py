import graphene

from .account.schema import AccountQueries

class Query(AccountQueries):
    node = graphene.Node.Field()


schema = graphene.Schema(query=Query)
