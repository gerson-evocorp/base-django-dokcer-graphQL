import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth import get_user_model

# Create your types here.
class UserType(DjangoObjectType):  
  class Meta:
    model = get_user_model()