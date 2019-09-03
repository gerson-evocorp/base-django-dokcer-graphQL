
from django.urls import path, include
from graphene_django.views import GraphQLView

urlpatterns = [
    path("graphql", GraphQLView.as_view(graphiql=True)),
    path("auth/",  include('apps.user.urls'))
]