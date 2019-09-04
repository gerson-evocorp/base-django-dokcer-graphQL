from graphene import relay
from django.contrib.auth import get_user_model
# from graphene_django.types import DjangoObjectType
from django_graphene_permissions import PermissionDjangoObjectType
from django_graphene_permissions.permissions import IsAuthenticated

class UserType(PermissionDjangoObjectType):  
  class Meta:
    model = get_user_model()
    interfaces = (relay.Node,)

  @staticmethod
  def permission_classes():
    return [IsAuthenticated]