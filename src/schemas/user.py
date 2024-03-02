from typing import Optional
from datetime import datetime , date
from pydantic import EmailStr

from schemas.base import BaseSchema


class UserSchema(BaseSchema):
    id: int
    email : EmailStr
    first_name:str
    last_name:str
    birth_date:date
    is_active : bool

    class Config:
        from_attributes = True