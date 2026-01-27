#!/bin/bash

# Load environment variables from .env file
if [ -f .env ]; then
    export $(cat .env | xargs)
else
    echo "Error: .env file not found"
    exit 1
fi

# Connect to PostgreSQL using Docker
docker run --rm -it \
    -e PGPASSWORD="$DB_PASSWORD" \
    postgres:15 \
    psql -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER" -d "$DB_NAME"
