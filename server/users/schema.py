import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from users.models import User


class UserConnection(graphene.relay.Connection):
    class Meta:
        abstract = True

    total_count = graphene.Int()
    edge_count = graphene.Int()

    def resolve_total_count(root, info, **kwargs):
        return root.length

    def resolve_edge_count(root, info, **kwargs):
        return len(root.edges)


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = ["email"]
        interfaces = (graphene.relay.Node,)
        connection_class = UserConnection


class Query(graphene.ObjectType):
    user = graphene.relay.Node.Field(UserNode)
    users = DjangoFilterConnectionField(UserNode)


class AddUser(graphene.relay.ClientIDMutation):
    class Input:
        email = graphene.String(required=True)
        password = graphene.String(required=True)
        is_superuser = graphene.Boolean()
        is_staff = graphene.Boolean()
        is_active = graphene.Boolean()

    user = graphene.Field(UserNode)

    @classmethod
    def mutate_and_get_payload(
        cls,
        root,
        info,
        email,
        password,
        is_superuser=False,
        is_staff=False,
        is_active=False,
    ):
        user = User(
            email=email,
            is_superuser=is_superuser,
            is_staff=is_staff,
            is_active=is_active,
        )
        user.set_password(password)
        user.save()
        return AddUser(user=user)


class DeleteUser(graphene.relay.ClientIDMutation):
    class Input:
        email = graphene.String()

    user = graphene.Field(UserNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, email):
        print(email)
        user = User.objects.get(email=email)
        user.delete()
        return DeleteUser(user=user)


class Mutation(graphene.ObjectType):
    add_user = AddUser.Field()
    delete_user = DeleteUser.Field()
