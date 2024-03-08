from contextlib import asynccontextmanager

from graphene import ObjectType, List , Schema

from db import get_db_session
from gql.types import UserObject, BookObject, ReviewObject, BurrowObject
from models import User , BorrowRecord , Book, Review
from sqlalchemy.future import select
from sqlalchemy.orm import Session, noload, joinedload , load_only

class Query(ObjectType):
    users = List(UserObject)
    # burrows = List(BurrowObject)


    @staticmethod
    async def resolve_users(root,info):
        async with asynccontextmanager(get_db_session)() as db:
            q = await db.execute(select(User).options(noload(User.borrow_record_user), noload(User.user_review)).limit(200))
            result = q.scalars().unique().all()
            await db.close()
        return result






gql_schema =  Schema(query=Query)