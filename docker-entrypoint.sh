#!/bin/bash

# Apply database migrations
echo "Apply database migrations"
alembic upgrade head

# Start server
echo "Starting server"
uvicorn --factory src.entrypoints.fastapi_app.main:create_app --host 0.0.0.0
