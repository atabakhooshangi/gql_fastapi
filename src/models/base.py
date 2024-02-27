import datetime
from typing import Any

from sqlalchemy import DateTime, Column, Integer, Boolean
from sqlalchemy.orm import as_declarative, declared_attr



class TimestampMixin(object):
    created_at = Column(DateTime(), default=datetime.datetime.now)
    updated_at = Column(DateTime(), onupdate=datetime.datetime.now)
    is_archive = Column(Boolean(), default=False)


@as_declarative()
class Base(TimestampMixin):
    id: Any = Column(Integer, primary_key=True, index=True)
    __name__: str
    __allow_unmapped__ = True
    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return cls.__name__.lower()

