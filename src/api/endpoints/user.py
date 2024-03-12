import logging
from typing import List
from fastapi import (
    APIRouter,
    Depends,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import noload, joinedload
from db import get_db_session
from models import User
from schemas import UserSchema

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/user/", name="user:user",response_model=List[UserSchema])
async def user(
        db: AsyncSession = Depends(get_db_session),
):
    q = await db.execute(select(User).options(noload(User.borrow_records_user),joinedload(User.user_reviews)).limit(5))
    result = q.scalars().unique().all()
    return result
