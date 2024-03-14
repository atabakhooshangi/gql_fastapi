
# GraphQL-Powered Book Library Application

This is an educational sample application for managing a book library system. It demonstrates the use of GraphQL with Graphene and FastAPI for creating a backend API. The application also showcases asynchronous database interactions using Async SQLAlchemy and employs Alembic for database migrations.

## Setup Instructions

### Prerequisites

- Python 3.11
- PostgreSQL database.
- `poetry` for Python package and environment management.

### Configuration

1. **Set up the Python environment**:

   Use Poetry to configure the virtual environment and install dependencies:

   ```bash
   poetry config virtualenvs.in-project true  # this will make poetry add the env folder to the directory of your toml file.
   poetry install
   poetry shell
   ```

   Alternatively, if you prefer using `pip`, there is  a `requirements.txt` file in the `src` folder you can install the dependencies like:

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables**:

   Create a `.env` file inside the `config` folder and add your PostgreSQL database credentials and application configuration:

   ```plaintext
   POSTGRES_USER=your-postgres-user
   POSTGRES_PASSWORD=your-postgres-password
   POSTGRES_SERVER=your-postgres-host
   POSTGRES_PORT=your-db-port
   POSTGRES_DB=your-db-name
   POSTGRES_SCHEME=postgresql+asyncpg
   ADD_MUTATION=0
   SERVER_PORT=your-desired-port
   RELOAD=True # or False
   ```

### Database Migrations

After creating and configuring your database connection, prepare the database for migrations:

1. Navigate to the `src` folder:

   ```bash
   cd src
   ```

2. Generate a new migration if there is any model change:

   ```bash
   alembic revision --autogenerate
   ```

3. Apply the migrations to your database:

   ```bash
   alembic upgrade head
   ```

   If the `versions` folder does not exist, It will automatically generate a versions folder in the `alembic` directory.

### Populating the Database with Fake Data

To populate your database with fake data:

```bash
python fake_data.py --users 1000 --books 5000 --borrow_records 1500 --reviews 5500 --clear --reset_indexes
```

- `--users`: Number of fake users to create.
- `--books`: Number of fake books to create.
- `--borrow_records`: Number of fake borrow records to create.
- `--reviews`: Number of fake reviews to create.
- `--clear`: Cleans up the database before inserting new data.
- `--reset_indexes`: Resets all indexes and creates a fresh database before inserting new data.


Adjust the numbers according to your needs.

### Running the Application

To run the application:

```bash
python main.py
```

Navigate to the host and port you have configured (e.g., `http://localhost:8000`) to access the GraphQL API interface.

## Sample GraphQL Queries Usage

### Fetching Users

To fetch users with optional filtering by `isActive`, `firstName`, `lastName`, `email`, and pagination controls (`skip`, `take`), you can use the following query:

```graphql
query {
  users(isActive: true, skip: 0, take: 10) {
    id
    email
    firstName
    lastName
    isActive
  }
}
```

### Fetching a Single User

To fetch a single user by `id` or `email`:

```graphql
query {
  user(id: 1) {
    id
    email
    firstName
    lastName
    borrowRecordsUser {
      borrowNote
      dueDate
      returnDate
    }
    userReviews {
      rating
      comment
    }
  }
}
```

### Fetching Borrow Records

To retrieve borrow records with optional filtering by `bookIdIn`, `userIdIn`, and pagination controls (`skip`, `take`):

```graphql
query {
  borrowsRecords(bookIdIn: [1, 2], skip: 0, take: 5) {
    id
    borrowNote
    dueDate
    returnDate
    user {
      id
      email
    }
    book {
      title
      author
    }
  }
}
```

### Fetching Books

To list books with optional filtering by `author`, `title`, and pagination controls (`skip`, `take`):

```graphql
query {
  books(author: "J.K. Rowling", skip: 0, take: 10) {
    id
    title
    author
    readersAvgRating
    averageBorrowedTime
  }
}
```

Each of these queries can be executed against your GraphQL endpoint to retrieve data from your book library application. Adjust the filter values and pagination controls as needed based on your data and requirements.

## Exploring the API with GraphQL Playground

<p>The GraphQL Playground provides an interactive UI to explore the API's schema and documentation. After starting the application and navigating to the GraphQL endpoint (`http://localhost:8000/`), You'll find the <span style="color: red;">"Docs"</span> and <span style="color: blue;">"Schema"</span> sections on the right side of the playground.These sections offer a comprehensive overview of the available queries, mutations, and their respective fields, arguments, and types. </p>

This feature is incredibly useful for understanding the capabilities of the API and for experimenting with queries and mutations in real-time.


## Additional Information

- Ensure the `.env` file is correctly placed and filled with your actual database and application settings.
- The `ADD_MUTATION=0` in the `.env` file can be adjusted based on your requirements to enable or disable specific mutations.


## Authors

* Atabak The NePhaLeM - *Initial work* - https://github.com/atabakhooshangi/gql_fastapi

## Deployed Version

* You can find this application deployed on vercel using Heroku Postgres DB here : https://library-gql-nephalem.vercel.app/