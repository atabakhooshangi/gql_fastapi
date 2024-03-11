from graphene import Schema

from .queries import Query
from .mutate import Mutation

gql_schema = Schema(query=Query, mutation=Mutation)
