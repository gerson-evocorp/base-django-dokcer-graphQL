import graphene
from .types import UserType
from django.contrib.auth.models import User

class Query(object):
    users = graphene.List(UserType)
    me = graphene.Field(UserType)

    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Não Autenticado!')

        return user