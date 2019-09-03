import graphene

#import querys
from apps.user.schema.query import Query as UserQuery

#import mutations
from apps.user.schema.mutation import Mutation as UserMutation

class Query(
    UserQuery
    ):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass

class Mutation(
    UserMutation
    ):
    # This class will inherit from multiple Queries
    # as we begin to add more apps to our project
    pass
