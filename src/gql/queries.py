from contextlib import asynccontextmanager

from graphene import ObjectType, List, Field, Argument, Boolean, String, Int

from db import get_db_session
from gql.types import UserObject, BookObject, ReviewObject, BurrowObject
from models import User, BorrowRecord, Book, Review
from sqlalchemy.future import select
from sqlalchemy.orm import Session, noload, joinedload, load_only
from sqlalchemy import asc, desc
from schemas import UserSchema

class ModelMapper:
    USER_MAPPER = {
        "is_active":User.is_active,
        "id":User.id,
        "first_name":User.first_name,
        "last_name":User.last_name,
        "email":User.email,
        "ids":User.id,
    }

def ordering(order:str):
    if order.startswith('-'):
        return desc(order[1:])
    return asc(order)

class Query(ObjectType):
    users = List(UserObject,
                 is_active=Argument(Boolean, required=False,default_value=True),
                 first_name=Argument(String, required=False),
                 last_name=Argument(String, required=False),
                 email=Argument(String, required=False),
                 ids=Argument(List(Int), required=False),
                 order_by=Argument(String, required=False,default_value='id'),
                 )
    user = Field(UserObject,
                 id=Int(required=False),
                 email=Argument(String, required=False))
    burrows = List(BurrowObject)

    @staticmethod
    async def resolve_users(root, info,**kwargs):
        order = kwargs.pop('order_by')
        print(order)
        filters = [ModelMapper.USER_MAPPER[key] == val if key != 'ids' else ModelMapper.USER_MAPPER[key].in_(val) for key,val in kwargs.items()]
        async with asynccontextmanager(get_db_session)() as db:
            query = select(User).options(noload(User.borrow_records_user), joinedload(User.user_reviews)).filter(*filters).order_by(ordering(order))
            q = await db.execute(
                query
            )
            result = q.scalars().unique().all()
        return result

    @staticmethod
    async def resolve_user(root, info,**kwargs):
        if not kwargs:
            raise Exception('Either one of id or email should be given')
        filters = [ModelMapper.USER_MAPPER[key] == val for key, val in kwargs.items()]
        async with asynccontextmanager(get_db_session)() as db:
            query = select(User).options(noload(User.borrow_records_user), joinedload(User.user_reviews)).filter(*filters)
            q = await db.execute(
                query
            )
            result = q.scalars().first()
        return result