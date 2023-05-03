import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from users.models import User


class UserNode(DjangoObjectType):
    class Meta:
        model = User
        filter_fields = ["email"]
        interfaces = (graphene.relay.Node,)


class UserInput(graphene.InputObjectType):
    id = graphene.Int()
    email = graphene.String()
    last_login = graphene.DateTime()
    is_superuser = graphene.Boolean()
    is_staff = graphene.Boolean()
    password = graphene.String()
    is_active = graphene.Boolean()
    date_joined = graphene.DateTime()


class Query(graphene.ObjectType):
    user = graphene.relay.Node.Field(UserNode)
    users = DjangoFilterConnectionField(UserNode)


class AddUser(graphene.relay.ClientIDMutation):
    class Input:
        user_data = UserInput(required=True)

    user = graphene.Field(UserNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, user_data=None):
        user = User(
            email=user_data.email,
            is_superuser=user_data.is_superuser,
            is_staff=user_data.is_staff,
            password=user_data.password,
        )
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
