import graphene
from .types import UserType
from django.contrib.auth.models import User
from django_graphene_permissions import permissions_checker
from django_graphene_permissions.permissions import IsAuthenticated
from name_projeto_manage.permissions import IsSuperUser

class Query(object):
    users = graphene.List(UserType)
    me = graphene.Field(UserType)

    @permissions_checker([IsSuperUser, IsAuthenticated])
    def resolve_users(self, info, **kwargs):
        return User.objects.all()

    @permissions_checker([IsAuthenticated])
    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Não autenticado!')

        return user