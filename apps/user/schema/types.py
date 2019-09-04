import graphene
from django.contrib.auth import get_user_model
from django_graphene_permissions import PermissionDjangoObjectType
from django_graphene_permissions.permissions import IsAuthenticated

# Create your types here.
class UserType(PermissionDjangoObjectType):  
  class Meta:
    model = get_user_model()
    
  @staticmethod
  def permission_classes():
    return [IsAuthenticated]