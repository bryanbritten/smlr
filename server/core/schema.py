import graphene
from links.schema import Query as LinkQuery
from links.schema import Mutation as LinkMutation
from users.schema import Query as UserQuery
from users.schema import Mutation as UserMutation


class Query(LinkQuery, UserQuery):
    pass


class Mutation(LinkMutation, UserMutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
