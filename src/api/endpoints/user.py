import logging
from datetime import datetime
from typing import Any, List

from fastapi import (
    APIRouter,
    Body,
    Depends,
    status,
    HTTPException,
    Request,
    Response
)

from fastapi.responses import ORJSONResponse
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import Session, noload, joinedload , load_only

from db import get_db_session
from models import User
from schemas import UserSchema

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/user/", name="user:user",response_model=List[UserSchema])
async def user(
        db: AsyncSession = Depends(get_db_session),
):
    q = await db.execute(select(User).options(noload(User.borrow_record_user),noload(User.user_review)))
    result = q.scalars().unique().all()
    return result
