from graphene import Int,String,Boolean , Date , Field
from graphene import ObjectType, List



class UserObject(ObjectType):
    id = Int()
    email = String()
    first_name = String()
    last_name = String()
    birth_date = Date()
    is_active = Boolean ()
    borrow_records_user = List(lambda: BurrowObject)
    user_reviews = List(lambda: ReviewObject)

    @staticmethod
    def resolve_borrow_records_user(root,info):
        return root.borrow_records_user

    @staticmethod
    async def resolve_user_reviews(root, info):
        return root.user_reviews

class BookObject(ObjectType):
    id= Int()
    title= String()
    author= String()
    serial_number= String()
    date_published= Date()
    pages= String()
    publisher= String()
    readers_avg_rating = Int()
    average_borrowed_time = Int()

class ReviewObject(ObjectType):
    id = Int()
    rating = String()
    comment = String()
    book = Field(lambda:BookObject)

    @staticmethod
    async def resolve_user_review(root, info):
        return root.book

class BurrowObject(ObjectType):
    id = Int()
    borrow_note = String()
    due_date = String()
    return_date = Date()
    user = Field(lambda: UserObject)
    book = Field(lambda: BookObject)

    @staticmethod
    def resolve_user(root,info):
        return root.user

    @staticmethod
    async def resolve_book(root, info):
        return root.book