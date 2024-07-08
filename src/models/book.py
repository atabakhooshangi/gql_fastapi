from typing import List

from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date, Text, CheckConstraint
from sqlalchemy.orm import relationship, validates, declared_attr , Mapped

from email_validator import validate_email
from .base import Base


class Book(Base):
    __tablename__ = 'books'
    __allow_unmapped__ = True
    id: Mapped[int] = Column(Integer, primary_key=True)
    title: Mapped[str] = Column(String(150))
    author: Mapped[str] = Column(String(150))
    serial_number: Mapped[str] = Column(String(100), index=True, unique=True)
    date_published: Mapped[Date] = Column(Date())
    pages: Mapped[str] = Column(String(4))
    publisher: Mapped[str] = Column(String(150))
    borrow_records: Mapped[List['BorrowRecord']] = relationship('BorrowRecord', uselist=True, lazy='selectin')
    book_review: Mapped['Review'] = relationship('Review', back_populates='book', lazy='selectin')

class BaseAssociation(Base):
    __abstract__ = True
    __allow_unmapped__ = True

    @declared_attr
    def user_id(cls) -> Mapped[int]:
        return Column('user_id', Integer, ForeignKey('users.id', ondelete="CASCADE"))

    @declared_attr
    def book_id(cls) -> Mapped[int]:
        return Column('book_id', Integer, ForeignKey('books.id', ondelete="CASCADE"))

    @declared_attr
    def user(cls) -> Mapped['User']:
        return relationship('User', back_populates='borrow_records_user', lazy='selectin')

    @declared_attr
    def book(cls) -> Mapped['Book']:
        return relationship('Book', back_populates='borrow_records', lazy='selectin')

class BorrowRecord(BaseAssociation):
    __tablename__ = 'borrow_records'
    id: Mapped[int] = Column(Integer, primary_key=True)
    borrow_note: Mapped[str] = Column(Text())
    due_date: Mapped[Date] = Column(Date())
    return_date: Mapped[Date] = Column(Date(), nullable=True)


class Review(BaseAssociation):
    __tablename__ = "reviews"
    id: Mapped[int] = Column(Integer, primary_key=True)
    rating: Mapped[int] = Column(Integer)
    comment: Mapped[str] = Column(Text())


    @declared_attr
    def user(cls) -> Mapped['User']:
        return relationship('User', back_populates='user_reviews', lazy='selectin')

    @declared_attr
    def book(cls) -> Mapped['Book']:
        return relationship('Book', back_populates='book_review', lazy='selectin')

    __allow_unmapped__ = True
    __table_args__ = (
        CheckConstraint('rating >= 1', name='rating_min'),
        CheckConstraint('rating <= 10', name='rating_max'),
    )
