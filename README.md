
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

## Additional Information

- Ensure the `.env` file is correctly placed and filled with your actual database and application settings.
- The `ADD_MUTATION=0` in the `.env` file can be adjusted based on your requirements to enable or disable specific mutations.


## Authors

* Atabak The NePhaLeM - *Initial work* - https://github.com/atabakhooshangi/gql_fastapi

## Deployed Version

* You can find this application deployed on vercel using Heroku Postgres DB here : https://library-gql-nephalem.vercel.app/