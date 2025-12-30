#!/bin/bash

set -e

echo "News 4U Backend - Starting..."

if [ ! -f "/app/data/news_4u.db" ] && [ ! -f "./news_4u.db" ]; then
    echo "Database not found. Initializing database with seed data..."
    python scripts/init_db.py
else
    echo "Database found. Skipping initialization."
    echo "Syncing feeds from configuration (idempotent)..."
    python scripts/init_db.py || echo "Warning: Feed sync failed, continuing anyway..."
fi

echo "Starting FastAPI server..."
exec uvicorn main:app --host 0.0.0.0 --port 8000 --log-level info

