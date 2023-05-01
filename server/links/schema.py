import graphene
from graphene_django import DjangoObjectType
from links.models import Link, Redirect
from users.models import User
from links import utils


class LinkType(DjangoObjectType):
    class Meta:
        model = Link
        fields = "__all__"


class RedirectType(DjangoObjectType):
    class Meta:
        model = Redirect
        fields = "__all__"


class LinkInput(graphene.InputObjectType):
    id = graphene.BigInt()
    link_id = graphene.BigInt()
    original = graphene.String()
    shortened = graphene.String()
    redirects = graphene.BigInt()
    created_at = graphene.DateTime()
    expires_at = graphene.DateTime()
    updated_at = graphene.DateTime()
    created_by = graphene.BigInt()


class RedirectInput(graphene.InputObjectType):
    id = graphene.BigInt()
    link_id = graphene.BigInt()
    referer = graphene.String()
    user_agent = graphene.String()
    ip_address = graphene.String()
    event_time = graphene.DateTime()


class Query(graphene.ObjectType):
    all_links = graphene.List(LinkType)
    link = graphene.Field(LinkType, id=graphene.BigInt())
    all_redirects = graphene.List(RedirectType)
    redirect = graphene.Field(RedirectType, id=graphene.BigInt())

    def resolve_all_links(self, info, email):
        user = User.objects.get(email=email)
        return Link.objects.get(created_by=user.id)

    def resolve_link(self, info, id):
        return Link.objects.get(pk=id)

    def resolve_all_redirects(self, info, link_id):
        return Redirect.objects.get(link_id=link_id)

    def resolve_redirect(self, info, id):
        return Redirect.objects.get(pk=id)


class AddLink(graphene.Mutation):
    class Arguments:
        link_data = LinkInput(required=True)

    link = graphene.Field(LinkType)

    @staticmethod
    def mutate(root, info, link_data=None):
        uuid = utils.generate_id()
        user = User.objects.get(pk=link_data.user_id)
        link_instance = Link(
            link_id=uuid,
            original=link_data.url,
            shortened=f"https://smlr.io/{utils.encode(uuid)}",
            created_by=user,
        )
        link_instance.save()
        return AddLink(link=link_instance)


class AddRedirect(graphene.Mutation):
    class Arguments:
        redirect_data = RedirectInput(required=True)

    redirect = graphene.Field(RedirectType)

    @staticmethod
    def mutate(root, info, redirect_data=None):
        redirect_instance = Redirect(
            link_id=redirect_data.link_id,
            referer=redirect_data.referer,
            user_agent=redirect_data.user_agent,
            ip_address=redirect_data.ip_address,
        )
        redirect_instance.save()
        return AddRedirect(redirect=redirect_instance)


class DeleteLink(graphene.Mutation):
    class Arguments:
        id = graphene.Int()

    link = graphene.Field(LinkType)

    @staticmethod
    def mutate(root, info, id):
        link_instance = Link.objects.get(link_id=id)
        link_instance.delete()
        return None


class Mutation(graphene.ObjectType):
    add_link = AddLink.Field()
    add_redirect = AddRedirect.Field()
    delete_link = DeleteLink.Field()
