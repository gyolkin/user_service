#!/bin/bash

echo "DB Connection --- Establishing . . ."

while ! nc -z $DB_HOST $DB_PORT; do
    sleep 1
    echo "Waiting for DB --- Retrying . . ."
done

echo "DB Connection --- Successfully Established!"
echo "DB Migrations --- Running . . ."

alembic upgrade head

echo "DB Migrations --- Successfully Migrated!"
echo "FastAPI Application --- Running . . ."

uvicorn src.user_service.main:create_production_app --host 0.0.0.0 --port 8000
