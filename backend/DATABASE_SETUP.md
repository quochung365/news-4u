# PostgreSQL Database Setup Guide

This document outlines the steps to set up the PostgreSQL database for the News 4U application.

## Option 1: Docker Setup (Recommended)

### Step 1: Install PostgreSQL
Pull the PostgreSQL image from Docker Hub:
```bash
docker pull postgres:15
```

### Step 2: Create a Docker Network
Create a Docker network to allow communication between the backend and the database:
```bash
docker network create news4u-network
```

### Step 3: Run the PostgreSQL Container
Run the PostgreSQL container with the following command:
```bash
docker run -d \
  --name news4u-db \
  --network news4u-network \
  -e POSTGRES_USER=news4u \
  -e POSTGRES_PASSWORD=news4u_password \
  -e POSTGRES_DB=news4u_db \
  -p 5432:5432 \
  postgres:15
```

### Step 4: Verify the Database is Running
Check if the PostgreSQL container is running:
```bash
docker ps
```
You should see the `news4u-db` container in the list. You can also connect to the database using a PostgreSQL client or via command line:
```bash
docker exec -it news4u-db psql -U news4u -d news4u_db
```

### Step 5: Update Backend Configuration
Create a `.env` file in the backend directory with the following content:
```env
DB_NAME=news4u_db
DB_USER=news4u
DB_PASS=news4u_password
DB_HOST=localhost
DB_PORT=5432
SCHEDULE_ENABLE=true
GEMINI_API_KEY=your_api_key_here
ARTICLE_EXTRACTION_MAX_RETRY=3
DEBUG_LEVEL=INFO
```

### Step 6: Create Tables
The application will automatically create tables when you start the backend server. The tables are defined in `models.py` and will be created via SQLAlchemy's `create_all()` method.

Alternatively, you can manually apply the SQL schema:
```bash
docker exec -i news4u-db psql -U news4u -d news4u_db < sql/create_schema.sql
```

### Step 7: Seed Initial Data (Optional)
If you have a seed data script, run it to populate the database with initial RSS feeds:
```bash
# Activate your virtual environment first
source venv/bin/activate

# Run seed script (if available)
python seed_data.py seed
```

---

## Option 2: Local PostgreSQL Setup

### Prerequisites
- PostgreSQL 15+ installed on your system

### Step 1: Install PostgreSQL

**macOS (using Homebrew):**
```bash
brew install postgresql@15
brew services start postgresql@15
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**Windows:**
Download and install from [postgresql.org](https://www.postgresql.org/download/windows/)

### Step 2: Create Database and User
```bash
# Connect to PostgreSQL as superuser
psql -U postgres

# In psql shell:
CREATE DATABASE news4u_db;
CREATE USER news4u_user WITH PASSWORD 'your_password_here';
GRANT ALL PRIVILEGES ON DATABASE news4u_db TO news4u_user;
\q
```

### Step 3: Update Backend Configuration
Create a `.env` file in the backend directory:
```env
DB_NAME=news4u_db
DB_USER=news4u_user
DB_PASS=your_password_here
DB_HOST=localhost
DB_PORT=5432
SCHEDULE_ENABLE=true
GEMINI_API_KEY=your_api_key_here
ARTICLE_EXTRACTION_MAX_RETRY=3
DEBUG_LEVEL=INFO
```

### Step 4: Apply Database Schema

**Option A: Automatic (via SQLAlchemy)**
```bash
# Simply start the backend server
# Tables will be created automatically
cd backend
source venv/bin/activate
uvicorn main:app --reload
```

**Option B: Manual (via SQL script)**
```bash
cd backend/sql
./apply_schema.sh
```

Or manually:
```bash
psql -h localhost -U news4u_user -d news4u_db -f sql/create_schema.sql
```

### Step 5: Verify Installation
```bash
# Connect to database
psql -h localhost -U news4u_user -d news4u_db

# List tables
\dt

# You should see:
# - rss_feeds
# - news_articles
# - feed_fetch_logs
```

---

## Database Schema

The application uses the following tables:

### `rss_feeds`
Stores RSS feed configuration.
- `id`: Primary key
- `name`: Feed name (unique)
- `url`: RSS feed URL
- `category`: News category
- `is_active`: Whether feed is active
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### `news_articles`
Stores processed news articles.
- `id`: Primary key
- `title`: Article title
- `summary`: Article summary
- `content`: Full article content
- `link`: Article URL (unique)
- `author`: Article author
- `published_date`: Publication date
- `category`: News category
- `image_url`: Featured image URL
- `slug`: Article slug
- `retry_count`: Content extraction retry count
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp
- `feed_id`: Foreign key to rss_feeds

### `feed_fetch_logs`
Stores RSS feed fetch operation logs.
- `id`: Primary key
- `feed_id`: Foreign key to rss_feeds
- `fetch_timestamp`: Fetch timestamp
- `status`: Operation status
- `articles_found`: Number of articles found
- `articles_processed`: Number of articles processed
- `error_message`: Error message if any
- `execution_time_ms`: Execution time in milliseconds

---

## Troubleshooting

### Connection Refused
```bash
# Check if PostgreSQL is running
# macOS:
brew services list | grep postgresql

# Ubuntu:
sudo systemctl status postgresql

# Restart if needed:
brew services restart postgresql@15  # macOS
sudo systemctl restart postgresql    # Ubuntu
```

### Authentication Failed
- Verify credentials in `.env` file match your PostgreSQL setup
- Check `pg_hba.conf` for authentication settings

### Database Already Exists
```bash
# Drop and recreate if needed (WARNING: deletes all data)
dropdb -U postgres news4u_db
createdb -U postgres news4u_db
```

### Permission Errors
```bash
# Grant permissions to user
psql -U postgres -d news4u_db
GRANT ALL PRIVILEGES ON DATABASE news4u_db TO news4u_user;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO news4u_user;
```

---

## Backup and Restore

### Backup Database
```bash
pg_dump -h localhost -U news4u_user news4u_db > backup_$(date +%Y%m%d).sql

# For Docker:
docker exec -t news4u-db pg_dump -U news4u news4u_db > backup_$(date +%Y%m%d).sql
```

### Restore Database
```bash
psql -h localhost -U news4u_user news4u_db < backup.sql

# For Docker:
docker exec -i news4u-db psql -U news4u -d news4u_db < backup.sql
```
