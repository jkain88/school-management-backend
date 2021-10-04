import graphene

from .account.schema import AccountQueries, AccountMutations

class Query(AccountQueries):
    node = graphene.Node.Field()

class Mutation(AccountMutations):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
