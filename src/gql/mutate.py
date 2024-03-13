from contextlib import asynccontextmanager

from graphene import Mutation, String, Int, Float, Date, Field , ObjectType

from config import settings
from db import get_db_session
from gql.types import BookObject
from models import Book


class AddBook(Mutation):
    class Arguments:
        title = String(required=True)
        author = String(required=True)
        serial_number = String(required=True)
        date_published = Date(required=True)
        pages = String(required=True)
        publisher = String(required=True)

    book = Field(BookObject)

    @staticmethod
    async def mutate(root, info, **kwargs):
        async with asynccontextmanager(get_db_session)() as db:
            book = Book(**kwargs)
            db.add(book)
            await db.commit()
            await db.refresh(book)
            return AddBook(book=book)


class Mutation(ObjectType):
    add_book=AddBook.Field()

MUTATE = {"mutation":Mutation} if settings.ADD_MUTATION == 1 else {}