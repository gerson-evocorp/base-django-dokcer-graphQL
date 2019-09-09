from django.urls import path, include
from graphene_django.views import GraphQLView
from .views.graphql import SafeGraphQLView
from django.views.decorators.csrf import csrf_exempt  

urlpatterns = [
    path("graphql", csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path("auth/",  include('apps.user.urls'))
]