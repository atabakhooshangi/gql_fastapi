#!/bin/bash

# Stop on error
set -e

# Run Alembic Upgrades
alembic revision --autogenerate

alembic upgrade head

# Populate database with fake data
python fake_data.py --users 1000 --books 5000 --borrow_records 1500 --reviews 5500 --clear --reset_indexes

# Start the FastAPI application
uvicorn main:app --host 0.0.0.0 --port ${PORT:-8888} --reload
