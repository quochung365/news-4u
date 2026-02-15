Description
This document outlines the steps to set up the container database for the News-4U application.

## Step 1: Install PostgreSQL
Pull the PostgreSQL image from Docker Hub:
```bash
docker pull postgres:15
```

## Step 2: Create a Docker Network
Create a Docker network to allow communication between the backend and the database:
```bash
docker network create news4u-network
```

## Step 3: Run the PostgreSQL Container
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

## Step 4: Verify the Database is Running
Check if the PostgreSQL container is running:
```bash
docker ps
```
You should see the `news4u-db` container in the list. You can also connect to the database using a PostgreSQL client or via command line:
```bash
docker exec -it news4u-db psql -U news4u -d news4u_db
```

## Step 5: Update Backend Configuration
Make sure to update the backend configuration (.env file) to connect to the PostgreSQL database.
```env
DB_NAME=news4u_db
DB_USER=news4u
DB_PASS=news4u_password
DB_HOST=news4u-host
DB_PORT=5432
```

## Step 6: Create tables and apply migrations
Run the following command to create tables and apply migrations:
```bash
docker exec -it news4u-backend python manage.py migrate
``` 



## Step 7: Seed Initial Data
Run the seed data script to populate the database with initial data:
```bash
docker exec -it news4u-backend python seed_data.py
```
