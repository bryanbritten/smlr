import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from links.models import Link, Redirect
from users.models import User
from links import utils


class LinkConnection(graphene.relay.Connection):
    class Meta:
        abstract = True

    total_count = graphene.Int()

    def resolve_total_count(root, info, **kwargs):
        return len(root.edges)


class LinkNode(DjangoObjectType):
    class Meta:
        model = Link
        filter_fields = {
            "original": ["exact", "icontains", "istartswith"],
            "created_by": ["exact"],
            "created_by__email": ["exact"],
        }
        interfaces = (graphene.relay.Node,)
        connection_class = LinkConnection


class RedirectNode(DjangoObjectType):
    class Meta:
        model = Redirect
        filter_fields = ["link_id", "referer"]
        interfaces = (graphene.relay.Node,)


class Query(graphene.ObjectType):
    link = graphene.Field(LinkNode, id=graphene.BigInt(required=True))
    links = DjangoFilterConnectionField(LinkNode)
    redirect = graphene.Field(RedirectNode, id=graphene.BigInt(required=True))
    redirects = DjangoFilterConnectionField(RedirectNode)


class AddLink(graphene.relay.ClientIDMutation):
    class Input:
        url = graphene.String(required=True)
        creator = graphene.String(required=True)

    link = graphene.Field(LinkNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, url, creator):
        uuid = utils.generate_id()
        user = User.objects.get(email=creator)
        link = Link(
            link_id=str(uuid),
            original=url,
            shortened=f"https://smlr.io/{utils.encode(uuid)}",
            created_by=user,
        )
        link.save()
        return AddLink(link=link)


class AddRedirect(graphene.relay.ClientIDMutation):
    class Input:
        link_id = graphene.BigInt()
        referer = graphene.String()
        user_agent = graphene.String()
        ip_address = graphene.String()

    redirect = graphene.Field(RedirectNode)

    @classmethod
    def mutate_and_get_payload(
        cls, root, info, link_id, referer, user_agent, ip_address
    ):
        redirect = Redirect(
            link_id=link_id,
            referer=referer,
            user_agent=user_agent,
            ip_address=ip_address,
        )
        redirect.save()
        return AddRedirect(redirect=redirect)


class DeleteLink(graphene.relay.ClientIDMutation):
    class Input:
        link_id = graphene.String(required=True)

    link = graphene.Field(LinkNode)

    @classmethod
    def mutate_and_get_payload(cls, root, info, link_id):
        link = Link.objects.get(link_id=link_id)
        link.delete()
        return DeleteLink(link=link)


class Mutation(graphene.ObjectType):
    add_link = AddLink.Field()
    add_redirect = AddRedirect.Field()
    delete_link = DeleteLink.Field()
