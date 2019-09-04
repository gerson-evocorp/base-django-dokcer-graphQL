import graphene
from django.contrib.auth import get_user_model
from graphene_django.types import DjangoObjectType
from django_graphene_permissions import permissions_checker
from django_graphene_permissions.permissions import IsAuthenticated, AllowAny
import graphql_jwt
from .types import UserType


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)

    class Arguments:
        username = graphene.String(required=True)
        password = graphene.String(required=True)
        email = graphene.String(required=True)

    @permissions_checker([AllowAny])
    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()

        return CreateUser(user=user)

class DeleteUser(graphene.Mutation):
    ok = graphene.Boolean()

    class Arguments:
        id = graphene.ID()

    @permissions_checker([IsAuthenticated])
    def mutate(self, info, id):
        instance = get_instance(id)
        instance.delete()
        return DeleteUser(ok=True)

class Mutation(graphene.ObjectType):
    # token_auth = graphql_jwt.ObtainJSONWebToken.Field()
    # verify_token = graphql_jwt.Verify.Field()
    # refresh_token = graphql_jwt.Refresh.Field()
    create_user = CreateUser.Field()
    delete_user = DeleteUser.Field()