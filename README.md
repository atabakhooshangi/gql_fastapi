
# A Book Library

This sample project demonstrates a functional book library system, designed as an educational example.
It utilizes GraphQL and Graphene for crafting API queries and mutations,
with FastAPI as the web framework to serve these APIs. The system manages data related to users,
books, borrow records, and reviews. Async SQLAlchemy is employed for database interactions,
showcasing asynchronous operations for improved efficiency.
Alembic is included for database migrations, 
facilitating easy adjustments to the database schema.


## Getting Started

These instructions will get your project up and running on your local machine for development and testing purposes.

### Prerequisites

What things you need to install the software and how to install them. This might include software like Python, Poetry, etc.

```
python --version
poetry --version
```

### Installing

A step-by-step series of examples that tell you how to get a development environment running. This should cover cloning the repo, installing dependencies via Poetry, and any other necessary steps.

```
git clone https://yourproject.git
cd yourproject
poetry install
```

## Setting Up the Database

Instructions for setting up your database, including running Alembic migrations to create or update the database schema.

```
alembic upgrade head
```

### Generating Fake Data

To populate your database with fake data for testing, use the `fake_data.py` script. This script allows you to specify the number of users, books, borrow records, and reviews to create. Additionally, you can use the `--clear` flag to clean up the database and the `--reset_indexes` flag to reset all indexes, which creates a fresh database and adds the new fake data.

```bash
python fake_data.py --users 1000 --books 5000 --borrow_records 1500 --reviews 5500 --clear --reset_indexes
```

- `--users`: Number of fake users to create.
- `--books`: Number of fake books to create.
- `--borrow_records`: Number of fake borrow records to create.
- `--reviews`: Number of fake reviews to create.
- `--clear`: Cleans up the database before inserting new data.
- `--reset_indexes`: Resets all indexes and creates a fresh database before inserting new data.

## Running the Server

How to run the server locally.

```
poetry run uvicorn app.main:app --reload
```

## Running Tests

Explain how to run the automated tests for this system.

```
poetry run pytest
```

## Deployment

Notes about how to deploy this on a live system.

## Contributing

Please read [CONTRIBUTING.md](https://yourproject.github.io/contributing) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://yourproject.github.io/tags).

## Authors

* **Your Name** - *Initial work* - [YourProfile](https://github.com/YourProfile)

See also the list of [contributors](https://yourproject.github.io/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

- Hat tip to anyone whose code was used
- Inspiration
- etc.
