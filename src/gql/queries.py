from contextlib import asynccontextmanager
from graphene import ObjectType, List, Field, Argument, Boolean, String, Int
from db import get_db_session
from gql.types import UserObject, BookObject, BurrowObject
from models import User, BorrowRecord, Book, Review
from sqlalchemy.future import select
from sqlalchemy.orm import noload, joinedload
from sqlalchemy import asc, desc, func, inspect, Date, case

class ModelMapper:
    """
    Provides mappings from GraphQL query parameters to SQLAlchemy model attributes.
    This facilitates the dynamic construction of filter expressions for queries.
    """

    # Mapping for user model attributes.
    USER_MAPPER = {
        "is_active": User.is_active,
        "id": User.id,
        "first_name": User.first_name,
        "last_name": User.last_name,
        "email": User.email,
        "id_in": User.id,
    }

    # Mapping for borrow record model attributes.
    BORROW_MAPPER = {
        "user_id_in": BorrowRecord.user_id,
        "book_id_in": BorrowRecord.book_id,
    }

    # Mapping for book model attributes.
    BOOK_MAPPER = {
        "author": Book.author,
        "title": Book.title,
        "id_in": Book.id,
    }

    @staticmethod
    def apply_pagination(query, skip=None, take=None):
        """
        Applies pagination to a SQLAlchemy query based on 'skip' (offset) and 'take' (limit) parameters.

        Parameters:
        - query: The SQLAlchemy query to modify.
        - skip: Optional; number of records to skip (offset) for pagination.
        - take: Optional; number of records to take (limit) for pagination.

        Returns:
        - The modified query with pagination applied.
        """
        if skip is not None:
            query = query.offset(skip)
        if take is not None:
            query = query.limit(take)
        return query

    @classmethod
    def get_filter_exp(cls, query_params: dict, mapper_name: str):
        """
        Constructs SQLAlchemy filter expressions based on provided query parameters
        using the specified attribute mapper.

        Parameters:
        - query_params: Dictionary of query parameters for filtering.
        - mapper_name: Name of the mapper to use (e.g., 'USER_MAPPER').

        Returns:
        - A list of SQLAlchemy filter expressions.
        """
        filter_expressions = []
        mapper = getattr(cls, mapper_name)  # Dynamically access the mapper based on mapper_name.

        for param, value in query_params.items():
            if param.endswith("_in") and param in mapper:
                # Ensures value is a list for 'in_' operations.
                if not isinstance(value, list):
                    raise ValueError(f"Expected a list for '{param}' but got '{type(value)}'")
                filter_expressions.append(mapper[param].in_(value))
            elif param in mapper:
                filter_expressions.append(mapper[param] == value)

        return filter_expressions
    @staticmethod
    def ordering(order: str):
        """
        Determines the SQLAlchemy ordering based on the provided string.

        Parameters:
        - order: A string indicating the ordering direction and field, prefixed with '-' for descending.

        Returns:
        - An SQLAlchemy ordering expression.
        """
        return desc(order[1:]) if order.startswith('-') else asc(order)

class Query(ObjectType):
    """
    GraphQL query class defining available queries and their resolvers.
    """

    # Users query with arguments for filtering and sorting.
    users = List(UserObject,
                 is_active=Argument(Boolean, required=False),
                 first_name=Argument(String, required=False),
                 last_name=Argument(String, required=False),
                 email=Argument(String, required=False),
                 id_in=Argument(List(Int), required=False),
                 limit=Argument(Int, required=False, default_value=100),
                 offset=Argument(Int, required=False, default_value=1),
                 order_by=Argument(String, required=False, default_value='id'),
                 skip=Argument(Int, required=False, default_value=0, description="Number of records to skip"),
                 take=Argument(Int, required=False, default_value=50, description="Number of records to take"),
                 )

    # Single user query with ID or email as argument.
    user = Field(UserObject,
                 id=Int(required=False),
                 email=Argument(String, required=False)
                 )

    # Borrow records query with filtering and sorting arguments.
    borrows_records = List(BurrowObject,
                           book_id_in=Argument(List(Int), required=False),
                           user_id_in=Argument(List(Int), required=False),
                           order_by=Argument(String, required=False, default_value='created_at'),
                           skip=Argument(Int, required=False, default_value=0, description="Number of records to skip"),
                           take=Argument(Int, required=False, default_value=50, description="Number of records to take"),
                           )

    # Books query with arguments for filtering.
    books = List(BookObject,
                 author=Argument(String, required=False),
                 title=Argument(String, required=False),
                 id_in=Argument(List(Int), required=False),
                 skip=Argument(Int, required=False,default_value=0, description="Number of records to skip"),
                 take=Argument(Int, required=False, default_value=50,description="Number of records to take"),
                 )

    @staticmethod
    async def resolve_books(root, info, **kwargs):
        """
        Resolves the books query to fetch books with optional filters applied.

        Returns a list of Book objects with additional computed fields for average rating and borrowed time.
        """
        skip = kwargs.pop('skip')
        take = kwargs.pop('take')
        async with asynccontextmanager(get_db_session)() as db:
            base_query = select(
                # Dynamically select all Book attributes.
                *[getattr(Book, column.name) for column in inspect(Book).c],
                # Calculate the average rating.
                func.coalesce(func.avg(Review.rating), 0).label('readers_avg_rating'),
                # Calculate the average borrowed time, treating missing return dates as zero.
                func.coalesce(func.sum(case(
                    (BorrowRecord.return_date.isnot(None),
                     func.cast(BorrowRecord.return_date, Date) - func.cast(BorrowRecord.created_at, Date)),
                    else_=0)), 0).label('average_borrowed_time')
            ).outerjoin(Review, Book.id == Review.book_id
            ).outerjoin(BorrowRecord, Book.id == BorrowRecord.book_id
            ).filter(*ModelMapper.get_filter_exp(kwargs, 'BOOK_MAPPER')
            ).group_by(Book.id)
            paginated_query = ModelMapper.apply_pagination(base_query,skip,take)
            result = await db.execute(paginated_query)
            return result.all()

    @staticmethod
    async def resolve_users(root, info, **kwargs):
        """
        Resolves the users query to fetch user entities with optional filters and sorting applied.
        """
        order = kwargs.pop('order_by')
        skip = kwargs.pop('skip')
        take = kwargs.pop('take')
        async with asynccontextmanager(get_db_session)() as db:
            base_query = select(User).options(
                joinedload(User.borrow_records_user),
                joinedload(User.user_reviews)
            ).filter(*ModelMapper.get_filter_exp(kwargs, 'USER_MAPPER')
            )
            paginated_query = ModelMapper.apply_pagination(base_query, skip, take)
            result = await db.execute(paginated_query.order_by(ModelMapper.ordering(order)))
            return result.scalars().unique().all()

    @staticmethod
    async def resolve_user(root, info, **kwargs):
        """
        Resolves the user query to fetch a single user entity based on provided ID or email.
        """
        if not kwargs:
            raise Exception('Either one of id or email should be given')
        async with asynccontextmanager(get_db_session)() as db:
            query = select(User).options(
                joinedload(User.borrow_records_user),
                joinedload(User.user_reviews)
            ).filter(*[ModelMapper.USER_MAPPER[key] == val for key, val in kwargs.items()])

            result = await db.execute(query)
            return result.scalars().first()

    @staticmethod
    async def resolve_borrows_records(root, info, **kwargs):
        """
        Resolves the borrows_records query to fetch borrowing records with optional filters and sorting.
        """
        order = kwargs.pop('order_by')
        skip = kwargs.pop('skip')
        take = kwargs.pop('take')
        async with asynccontextmanager(get_db_session)() as db:
            base_query = select(BorrowRecord).options(
                joinedload(BorrowRecord.user),
                joinedload(BorrowRecord.book)
            ).filter(*ModelMapper.get_filter_exp(kwargs, 'BORROW_MAPPER')
            ).order_by(ModelMapper.ordering(order))
            paginated_query = ModelMapper.apply_pagination(base_query, skip, take)
            result = await db.execute(paginated_query)
            return result.scalars().unique().all()
