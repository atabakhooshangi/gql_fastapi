from graphene import Schema

from .queries import Query
from .mutate import MUTATE

gql_schema = Schema(query=Query,**MUTATE)
