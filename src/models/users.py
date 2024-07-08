from typing import List

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship, validates, Mapped
from email_validator import validate_email
from .base import Base


class User(Base):
    __tablename__ = 'users'  # Define a table name for clarity
    __allow_unmapped__ = True
    id: Mapped[int] = Column(Integer, primary_key=True)  # Assuming there's an ID column
    email: Mapped[str] = Column(String(100), index=True, unique=True)
    password: Mapped[str] = Column(String(250))
    first_name: Mapped[str] = Column(String(150))
    last_name: Mapped[str] = Column(String(150))
    birth_date: Mapped[Date] = Column(Date())
    is_active: Mapped[bool] = Column(Boolean(), default=True)

    borrow_records_user: Mapped[List['BorrowRecord']] = relationship('BorrowRecord', uselist=True, lazy='selectin')
    user_reviews: Mapped[List["Review"]] = relationship('Review', uselist=True, lazy='selectin')

    @validates('email')
    def validate_email(self, key, email):
        try:
            validated_email = validate_email(email, check_deliverability=False).email
        except Exception as e:
            raise ValueError("Invalid email") from e
        return validated_email
