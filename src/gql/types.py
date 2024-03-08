from contextlib import asynccontextmanager

from graphene import ObjectType,List , Int,String,Boolean , Date , Field
from graphene import ObjectType, List , Schema

from db import get_db_session
from models import User , BorrowRecord , Book, Review
from sqlalchemy.future import select
from sqlalchemy.orm import Session, noload, joinedload , load_only


class UserObject(ObjectType):
    id = Int()
    email = String()
    first_name = String()
    last_name = String()
    birth_date = Date()
    is_active = Boolean ()
    # borrow_record_user = List(lambda: BurrowObject)
    user_review = List(lambda: ReviewObject)

    # @staticmethod
    # def resolve_borrow_record_user(root,info):
    #     return root.borrow_record_user

    @staticmethod
    async def resolve_user_review(root, info):
        async with asynccontextmanager(get_db_session)() as db:
            q = await db.execute(select(Review).options(noload(Review.user)).filter(Review.user_id == root.id))
            result = q.scalars().unique().all()
        # await db.close()
        return result

class BookObject(ObjectType):
    id= Int()
    title= String()
    author= String()
    serial_number= String()
    date_published= Date()
    pages= String()
    publisher= String()


class ReviewObject(ObjectType):
    id = Int()
    rating = String()
    comment = String()
    book = Field(lambda:BookObject)

class BurrowObject(ObjectType):
    id = Int()
    borrow_note = String()
    due_date = String()
    return_date = Field(lambda:BookObject)
    user = List(lambda: UserObject)
    book = List(lambda: BookObject)