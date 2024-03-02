from typing import Optional
from datetime import datetime
from pydantic import BaseModel


class BaseSchema(BaseModel):

    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
