from typing import Optional , List , Any
from datetime import datetime , date
from pydantic import EmailStr

from schemas.base import BaseSchema
from pydantic import BaseModel
class ReviewSchema(BaseModel):
    id:int
    # comment : str

    class Config:
        from_attributes = True

class UserSchema(BaseSchema):
    # id: int
    email : EmailStr
    # first_name:str
    # last_name:str
    # birth_date:date
    # is_active : bool
    user_reviews : List[ReviewSchema] = []

    class Config:
        from_attributes = True


