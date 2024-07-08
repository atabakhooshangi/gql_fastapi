import argparse
from faker import Faker
from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import sessionmaker, relationship

# Define your models here or import them if they are defined in a separate file
from config import settings
from models import User, Book, BorrowRecord
from models.book import Review

Base = declarative_base()
fake = Faker()

# Command-line argument setup
parser = argparse.ArgumentParser(description='Generate mock data for database.')
parser.add_argument('--users', type=int, help='Number of users to generate', default=100)  # --users 1000
parser.add_argument('--books', type=int, help='Number of books to generate', default=100)  # --books 1000
parser.add_argument('--borrow_records', type=int, help='Number of borrow records to generate', default=100)  # --borrow_records 1000
parser.add_argument('--reviews', type=int, help='Number of reviews to generate', default=100)  # --reviews 1000
parser.add_argument('--clear', action='store_true', help='Clear tables before generating new data')  # --clear
parser.add_argument('--reset_indexes', action='store_true', help='Reset PostgreSQL sequence indexes')  # --reset_indexes

#  python fake_data.py --users 1000 --books 5000 --borrow_records 1500 --reviews 5500 --clear --reset_indexes
args = parser.parse_args()

# Database setup
engine = create_engine(settings.get_sync_connection_url())  # Update with your database
Session = sessionmaker(bind=engine)
session = Session()


class GenerateFakeData:

    def create_fake_users(self, n):
        users = [
            User(
                email=fake.unique.ascii_free_email(),
                password=fake.password(length=12),
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                birth_date=fake.date_of_birth(tzinfo=None, minimum_age=18, maximum_age=90),
                is_active=fake.boolean()
            ) for _ in range(n)
        ]
        session.add_all(users)
        session.commit()

    def create_fake_books(self, n):
        books = [
            Book(
                title=fake.sentence(nb_words=5),
                author=fake.name(),
                serial_number=fake.unique.bothify(text='???-########'),
                date_published=fake.date_between(start_date='-30y', end_date='today'),
                pages=str(fake.random_int(min=100, max=1000)),
                publisher=fake.company()
            ) for _ in range(n)
        ]
        session.add_all(books)
        session.commit()

    def create_fake_borrow_records(self, n):
        users = session.query(User).all()
        books = session.query(Book).all()

        for _ in range(n):
            borrow_record = BorrowRecord(
                user_id=fake.random.choice(users).id,
                book_id=fake.random.choice(books).id,
                borrow_note=fake.text(max_nb_chars=200),
                due_date=fake.future_date(end_date="+30d"),
                return_date=fake.date_between(start_date='-30d', end_date='today') if fake.boolean(chance_of_getting_true=25) else None
            )
            session.add(borrow_record)
        session.commit()

    def create_fake_reviews(self, n):
        users = session.query(User).all()
        books = session.query(Book).all()

        for _ in range(n):
            review = Review(
                user_id=fake.random.choice(users).id,
                book_id=fake.random.choice(books).id,
                rating=fake.random_int(min=1, max=10),
                comment=fake.text(max_nb_chars=500)
            )
            session.add(review)
        session.commit()

    def clear_tables(self):
        session.execute(text("TRUNCATE TABLE reviews ,borrow_records ,books,users CASCADE;"))
        session.commit()
        print("Tables cleared.")

    def reset_postgres_indexes(self):
        session.execute(text("ALTER SEQUENCE users_id_seq RESTART WITH 1;"))
        session.execute(text("ALTER SEQUENCE books_id_seq RESTART WITH 1;"))
        session.execute(text("ALTER SEQUENCE borrow_records_id_seq RESTART WITH 1;"))
        session.execute(text("ALTER SEQUENCE reviews_id_seq RESTART WITH 1;"))
        session.commit()
        print("PostgreSQL sequence indexes reset.")


if __name__ == "__main__":
    Base.metadata.create_all(engine)  # Ensure all tables are created
    faker_instance = GenerateFakeData()
    if args.clear:  # Truncate Tables
        faker_instance.clear_tables()
        if args.reset_indexes:  # Reset Index Sequences
            faker_instance.reset_postgres_indexes()
    if args.users:
        faker_instance.create_fake_users(args.users)
    if args.books:
        faker_instance.create_fake_books(args.books)
    if args.borrow_records and args.users and args.books:
        faker_instance.create_fake_borrow_records(args.borrow_records)
    if args.reviews and args.users and args.books:
        faker_instance.create_fake_reviews(args.reviews)
