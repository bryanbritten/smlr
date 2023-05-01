import graphene
from graphene_django import DjangoObjectType
from users.models import User


class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = "__all__"


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
    user = graphene.Field(UserType, email=graphene.String())

    def resolve_user(self, info, email):
        return User.objects.get(email=email)


class AddUser(graphene.Mutation):
    class Arguments:
        user_data = UserInput(required=True)

    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, user_data=None):
        user_instance = User(
            email=user_data.email,
            is_superuser=user_data.is_superuser,
            is_staff=user_data.is_staff,
        )
        user_instance.save()
        return AddUser(user=user_instance)


class DeleteUser(graphene.Mutation):
    class Arguments:
        email = graphene.String()

    user = graphene.Field(UserType)

    @staticmethod
    def mutate(root, info, email):
        user_instance = User.objects.get(email=email)
        user_instance.delete()
        return None


class Mutation(graphene.ObjectType):
    add_user = AddUser.Field()
    delete_user = DeleteUser.Field()
