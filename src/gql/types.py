from graphene import ObjectType,List , Int,String,Boolean , Date , Field

class UserObject(ObjectType):
    id = Int()
    email = String()
    first_name = String()
    last_name = String()
    birth_date = Date()
    is_active = Boolean ()
    borrow_record_user = List(lambda: BurrowObject)
    user_review = List(lambda: ReviewObject)

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