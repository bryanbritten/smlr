import graphene
from graphene_django.debug import DjangoDebug
from links.schema import Query as LinkQuery
from links.schema import Mutation as LinkMutation
from users.schema import Query as UserQuery
from users.schema import Mutation as UserMutation


class Query(LinkQuery, UserQuery, graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name="_debug")


class Mutation(LinkMutation, UserMutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
