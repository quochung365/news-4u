# News 4U - Complete Documentation

## Table of Contents

1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Project Structure](#project-structure)
4. [Technology Stack](#technology-stack)
5. [Features](#features)
6. [Backend Documentation](#backend-documentation)
7. [Frontend Documentation](#frontend-documentation)
8. [Database Schema](#database-schema)
9. [API Documentation](#api-documentation)
10. [Setup & Installation](#setup--installation)
11. [Development Guide](#development-guide)
12. [Deployment](#deployment)

---

## Project Overview

**News 4U** is a comprehensive RSS news aggregation platform that automatically fetches, processes, and displays news articles from multiple RSS feeds across different categories. The system is designed with a modern microservices architecture, featuring a FastAPI backend and a Next.js frontend.

### Key Capabilities

- **Automated RSS Feed Fetching**: Scheduled fetching of news from multiple RSS sources
- **Content Extraction**: Intelligent extraction of full article content from source websites
- **Categorization**: Automatic categorization of news articles (Tech, Global News, Vietnamese News, US News)
- **Search & Filter**: Advanced search and filtering capabilities
- **Feed Management**: Dynamic feed management with enable/disable functionality
- **Responsive UI**: Modern, responsive web interface with dark mode support

### Target Users

- News enthusiasts who want to aggregate content from multiple sources
- Developers learning full-stack development
- Anyone interested in RSS feed aggregation and content processing

---

## Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                        Frontend (Next.js)                    │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Pages      │  │  Components  │  │   API Client │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────────────┬─────────────────────────────────┘
                             │ HTTP/REST API
┌────────────────────────────▼─────────────────────────────────┐
│                    Backend (FastAPI)                        │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Routers   │  │   Services   │  │   Models      │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Scheduler  │  │  Extractors  │  │   Database   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└────────────────────────────┬─────────────────────────────────┘
                             │
┌────────────────────────────▼─────────────────────────────────┐
│                    SQLite Database                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │ RSS Feeds   │  │   Articles   │  │ Fetch Logs   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Feed Fetching Flow**:
   ```
   Scheduler → RSS Service → Fetch RSS Feed → Parse Entries → 
   Extract Metadata → Store in Database → Log Results
   ```

2. **Content Extraction Flow**:
   ```
   Article Request → Check Content → Site Extractor → 
   Extract Content → Update Database → Return Article
   ```

3. **User Request Flow**:
   ```
   Frontend → API Request → Router → Service → Database → 
   Process Data → Return Response → Frontend Display
   ```

---

## Project Structure

### Overall Directory Structure

```
news-4u/
├── backend/                    # FastAPI backend application
│   ├── config/                # Configuration files
│   │   └── rss_feeds.py       # RSS feed definitions
│   ├── models/                # SQLAlchemy ORM models
│   │   └── database.py        # Database table definitions
│   ├── routers/                # FastAPI route handlers
│   │   └── news.py            # News API endpoints
│   ├── schemas/                # Pydantic validation schemas
│   │   └── news.py            # Request/response models
│   ├── services/               # Business logic layer
│   │   ├── rss_service.py     # RSS feed processing
│   │   ├── scheduler_service.py # Task scheduling
│   │   └── site_extractors.py  # Content extraction
│   ├── scripts/                # Utility scripts
│   │   ├── init_db.py         # Database initialization
│   │   └── ...                 # Migration scripts
│   ├── lib/                    # Utility functions
│   │   └── utils.py           # Helper functions
│   ├── main.py                 # FastAPI app entry point
│   ├── database.py             # Database connection setup
│   ├── requirements.txt        # Python dependencies
│   └── Dockerfile              # Docker configuration
│
├── frontend/                   # Next.js frontend application
│   ├── app/                    # Next.js app directory
│   │   ├── page.tsx            # Home page
│   │   ├── article/[slug]/     # Article detail pages
│   │   ├── layout.tsx          # Root layout
│   │   └── globals.css         # Global styles
│   ├── components/             # React components
│   │   ├── ArticleCard.tsx    # Article card component
│   │   ├── SearchBar.tsx      # Search component
│   │   ├── Pagination.tsx     # Pagination component
│   │   ├── FeedManager.tsx     # Feed management UI
│   │   └── DarkModeToggle.tsx  # Dark mode switcher
│   ├── lib/                    # Utility libraries
│   │   ├── api.ts             # API client
│   │   ├── utils.ts           # Helper functions
│   │   └── constants.ts        # Constants
│   ├── package.json           # Node.js dependencies
│   └── Dockerfile             # Docker configuration
│
├── docker-compose.yml         # Docker Compose configuration
├── README.md                   # Quick start guide
└── DOCUMENTATION.md           # This file
```

---

## Technology Stack

### Backend

- **Framework**: FastAPI 0.104.1
- **Language**: Python 3.9+
- **Database**: SQLite (with PostgreSQL support via Docker)
- **ORM**: SQLAlchemy 2.0.23
- **Validation**: Pydantic 2.5.2
- **RSS Parsing**: feedparser 6.0.10
- **HTTP Client**: httpx 0.27.2
- **HTML Parsing**: BeautifulSoup4 4.12.2
- **Content Extraction**: Newspaper3k 0.2.8
- **Scheduling**: APScheduler 3.10.4
- **Server**: Uvicorn

### Frontend

- **Framework**: Next.js 14.2.30
- **Language**: TypeScript 5.3.3
- **UI Library**: React 18.2.0
- **Styling**: Tailwind CSS 3.4.1
- **HTTP Client**: Axios 1.6.7
- **Icons**: Lucide React 0.330.0
- **Date Handling**: date-fns 3.3.1

### DevOps

- **Containerization**: Docker & Docker Compose
- **Database**: SQLite (development) / PostgreSQL (production)

---

## Features

### Core Features

#### 1. RSS Feed Management
- **Feed Configuration**: Centralized RSS feed configuration in `config/rss_feeds.py`
- **Multiple Categories**: Support for Tech, Global News, Vietnamese News, and US News
- **Feed Status**: Enable/disable feeds dynamically
- **Feed Addition**: Add new feeds via API or configuration
- **Feed Deletion**: Remove feeds from the system

#### 2. Automated Feed Fetching
- **Scheduled Fetching**: Automatic RSS feed fetching every 5 minutes
- **Manual Trigger**: On-demand feed fetching via API
- **Batch Processing**: Efficient batch processing of multiple feeds
- **Error Handling**: Robust error handling with retry logic
- **Fetch Logging**: Comprehensive logging of all fetch operations

#### 3. Article Processing
- **Metadata Extraction**: Extract title, summary, author, published date, images
- **Content Extraction**: Intelligent full-content extraction from source websites
- **Site-Specific Extractors**: Custom extractors for major news sites
- **Fallback Mechanism**: Multiple extraction strategies with fallbacks
- **Deduplication**: Prevent duplicate articles using unique link constraints
- **Slug Generation**: SEO-friendly URL slugs for articles

#### 4. Content Extraction
- **Multi-Strategy Extraction**: 
  - Site-specific extractors (VnExpress, TechCrunch, BBC, etc.)
  - Newspaper3k fallback
  - BeautifulSoup parsing
- **Image Extraction**: Extract featured images from articles
- **Content Cleaning**: Remove ads, unwanted elements, and format content
- **Lazy Loading**: Extract content on-demand when article is viewed

#### 5. Search & Filtering
- **Full-Text Search**: Search across title, summary, and content
- **Category Filtering**: Filter articles by category
- **Source Filtering**: Filter by news source
- **Feed Filtering**: Filter by specific RSS feeds
- **Time-Based Filtering**: Filter by time ranges (24h, 7d, 30d)
- **Pagination**: Efficient pagination for large result sets

#### 6. User Interface
- **Responsive Design**: Mobile-first responsive design
- **Dark Mode**: Full dark mode support with persistence
- **Category Navigation**: Easy category switching
- **Article Cards**: Beautiful article card layout
- **Article Detail Pages**: Dedicated pages for full article reading
- **Feed Manager**: UI for managing RSS feeds
- **Search Interface**: Advanced search with filters
- **Pagination**: User-friendly pagination controls

#### 7. Scheduler System
- **Feed Fetching Job**: Runs every 5 minutes
- **Content Extraction Job**: Runs every minute for articles without content
- **Job Management**: Start/stop scheduler via API
- **Status Monitoring**: Check scheduler and job status

#### 8. Admin Features
- **Data Cleanup**: Clean up all data or specific feed data
- **Article Management**: Delete article content
- **Feed Management**: Toggle feed status, delete feeds
- **Statistics**: View system statistics

### Advanced Features

#### 1. Performance Optimizations
- **Batch Database Operations**: Efficient batch inserts with conflict resolution
- **Slug Caching**: Cache existing slugs to prevent duplicates
- **Connection Pooling**: Database connection pooling
- **Async Processing**: Asynchronous feed fetching and content extraction

#### 2. Error Handling
- **Retry Logic**: Automatic retry with exponential backoff
- **Error Logging**: Comprehensive error logging
- **Graceful Degradation**: System continues operating even if some feeds fail
- **User-Friendly Errors**: Clear error messages for users

#### 3. Data Integrity
- **Unique Constraints**: Prevent duplicate articles
- **Data Validation**: Pydantic schemas for request/response validation
- **Transaction Management**: Proper database transaction handling
- **Data Migration**: Scripts for database migrations

---

## Backend Documentation

### Directory Structure

```
backend/
├── config/
│   └── rss_feeds.py          # RSS feed configuration and categories
├── models/
│   └── database.py           # SQLAlchemy ORM models (RSSFeed, NewsArticle, FeedFetchLog)
├── routers/
│   └── news.py               # All API route handlers
├── schemas/
│   └── news.py               # Pydantic models for validation
├── services/
│   ├── rss_service.py        # Core RSS feed processing logic
│   ├── scheduler_service.py   # Task scheduling with APScheduler
│   └── site_extractors.py     # Site-specific content extractors
├── scripts/
│   ├── init_db.py            # Database initialization script
│   └── ...                    # Migration and utility scripts
├── lib/
│   └── utils.py              # Utility functions (slug generation, etc.)
├── main.py                    # FastAPI application entry point
├── database.py                # Database connection and session management
└── requirements.txt           # Python dependencies
```

### Key Components

#### 1. Main Application (`main.py`)

**Purpose**: FastAPI application entry point with lifecycle management.

**Key Features**:
- Application initialization
- Database setup on startup
- RSS feed synchronization
- Scheduler lifecycle management
- CORS middleware configuration
- Global exception handling

**Lifecycle Events**:
- **Startup**: Initialize database, sync RSS feeds, start scheduler
- **Shutdown**: Stop scheduler gracefully

#### 2. Database Models (`models/database.py`)

**RSSFeed Model**:
- Stores RSS feed configuration
- Fields: id, name, url, category, is_active, timestamps
- Indexes on category and is_active

**NewsArticle Model**:
- Stores processed news articles
- Fields: id, title, summary, content, link, author, published_date, category, source_name, source_url, image_url, slug, is_processed, timestamps
- Unique constraint on link and slug
- Multiple indexes for performance

**FeedFetchLog Model**:
- Logs RSS feed fetch operations
- Fields: id, feed_name, fetch_timestamp, status, articles_found, articles_processed, error_message, execution_time
- Indexes on feed_name, timestamp, and status

#### 3. RSS Service (`services/rss_service.py`)

**Core Responsibilities**:
- Fetch RSS feeds asynchronously
- Parse RSS feed entries
- Extract article metadata
- Process articles in batches
- Extract full article content
- Handle deduplication
- Manage feed operations

**Key Methods**:
- `fetch_feed_async()`: Fetch and process a single RSS feed
- `fetch_all_feeds()`: Fetch all active feeds
- `extract_article_content()`: Extract full content from article URL
- `_process_articles_batch()`: Batch process articles with deduplication
- `toggle_feed_status()`: Enable/disable feeds
- `delete_feed()`: Remove feeds

**Extraction Strategy**:
1. Try site-specific extractor
2. Fallback to Newspaper3k
3. Fallback to BeautifulSoup parsing

#### 4. Site Extractors (`services/site_extractors.py`)

**Purpose**: Site-specific content extraction for better accuracy.

**Supported Sites**:
- Vietnamese: VnExpress, TuoiTre, Kenh14
- Tech: TechCrunch, The Verge, Engadget
- Global: BBC, CNBC, CBS News
- US: ABC News, NBC News

**Base Extractor Features**:
- HTML sanitization
- Ad removal
- Unwanted element removal
- Image tag cleaning
- Content formatting

#### 5. Scheduler Service (`services/scheduler_service.py`)

**Purpose**: Manage scheduled tasks for feed fetching and content extraction.

**Scheduled Jobs**:
1. **Feed Fetching Job**: Runs every 5 minutes
   - Fetches all active RSS feeds
   - Processes new articles
   - Logs results

2. **Content Extraction Job**: Runs every minute
   - Finds articles without content
   - Extracts content for top 20 latest articles
   - Updates database

**Job Management**:
- Start/stop scheduler
- Check job status
- View next run times

#### 6. API Routers (`routers/news.py`)

**Route Categories**:

1. **Feed Endpoints** (`/api/news/feeds/*`):
   - `GET /feeds`: Get all feeds
   - `GET /feeds/logs`: Get fetch logs
   - `GET /feeds/status`: Get feed status
   - `POST /feeds/{feed_name}/toggle`: Toggle feed status
   - `DELETE /feeds/delete/{feed_name}`: Delete feed
   - `POST /feeds/add`: Add new feed

2. **Article Endpoints** (`/api/news/articles/*`):
   - `GET /articles`: Get articles with filters
   - `GET /articles/{article_id}`: Get article by ID
   - `GET /articles/slug/{slug}`: Get article by slug
   - `GET /articles/category/{category}`: Get articles by category
   - `POST /articles/{article_id}/extract`: Extract article content

3. **Search Endpoints** (`/api/news/search`):
   - `GET /search`: Search articles with filters

4. **Fetch Endpoints** (`/api/news/fetch/*`):
   - `POST /fetch`: Fetch all feeds
   - `POST /fetch/{feed_name}`: Fetch specific feed

5. **Scheduler Endpoints** (`/api/news/scheduler/*`):
   - `GET /scheduler/status`: Get scheduler status
   - `POST /scheduler/start`: Start scheduler
   - `POST /scheduler/stop`: Stop scheduler

6. **Stats Endpoints** (`/api/news/stats`, `/api/news/health`):
   - `GET /health`: Health check
   - `GET /stats`: Get statistics

7. **Admin Endpoints** (`/api/news/admin/*`):
   - `DELETE /admin/cleanup/all`: Clean all data
   - `DELETE /admin/cleanup/feed/{feed_name}`: Clean feed data
   - `DELETE /admin/cleanup/article/{article_id}`: Delete article content

#### 7. Configuration (`config/rss_feeds.py`)

**News Categories**:
- `TECH`: Technology news
- `GLOBAL_NEWS`: Global/world news
- `VIETNAMESE_NEWS`: Vietnamese news
- `US_NEWS`: US news

**RSS Feed Structure**:
- Name, URL, Category, Active status
- Organized by category in dictionary

**Helper Functions**:
- `get_all_feeds()`: Get all feeds as flat list
- `get_active_feeds()`: Get only active feeds
- `get_feed_by_name()`: Get specific feed by name

---

## Frontend Documentation

### Directory Structure

```
frontend/
├── app/                       # Next.js app directory
│   ├── page.tsx              # Home page with article listing
│   ├── article/[slug]/
│   │   └── page.tsx          # Article detail page
│   ├── layout.tsx            # Root layout with metadata
│   └── globals.css           # Global styles and Tailwind
├── components/                # React components
│   ├── ArticleCard.tsx       # Article card display
│   ├── SearchBar.tsx         # Search interface
│   ├── Pagination.tsx        # Pagination controls
│   ├── FeedManager.tsx       # Feed management UI
│   ├── DarkModeToggle.tsx    # Dark mode switcher
│   └── Footer.tsx            # Footer component
└── lib/                      # Utility libraries
    ├── api.ts                # API client functions
    ├── utils.ts              # Helper functions
    ├── constants.ts          # Constants and mappings
    └── darkMode.tsx          # Dark mode utilities
```

### Key Components

#### 1. Home Page (`app/page.tsx`)

**Features**:
- Article listing with pagination
- Category filtering
- Feed filtering
- Search functionality
- State persistence (localStorage + URL)
- Responsive grid layout

**State Management**:
- Articles list
- Selected category
- Selected feeds
- Search query and results
- Pagination state
- Loading states

**User Interactions**:
- Category selection
- Feed selection
- Search
- Article click navigation
- Pagination

#### 2. Article Detail Page (`app/article/[slug]/page.tsx`)

**Features**:
- Full article display
- Automatic content extraction if missing
- Image display
- Author and date information
- Source attribution
- Back navigation

#### 3. Article Card (`components/ArticleCard.tsx`)

**Displays**:
- Article title
- Summary/excerpt
- Featured image
- Source name
- Published date
- Category badge

**Interactions**:
- Click to view full article
- Loading state during content extraction

#### 4. Search Bar (`components/SearchBar.tsx`)

**Features**:
- Search input
- Category filter dropdown
- Time filter dropdown (24h, 7d, 30d)
- Clear search button
- Loading indicator

#### 5. Feed Manager (`components/FeedManager.tsx`)

**Features**:
- List all available feeds
- Toggle feed active status
- Visual indicators for active/inactive feeds
- Category grouping
- Apply feed filter

#### 6. API Client (`lib/api.ts`)

**Functions**:
- `getArticles()`: Fetch articles with filters
- `getArticleBySlug()`: Get article by slug
- `getArticlesByCategory()`: Get articles by category
- `getFeeds()`: Get all feeds
- `extractArticleContent()`: Trigger content extraction
- `searchArticles()`: Search articles

**Features**:
- Axios instance with base URL
- Request/response interceptors
- Error handling
- TypeScript types

---

## Database Schema

### Tables

#### 1. `rss_feeds`

Stores RSS feed configuration.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| name | VARCHAR(255) | UNIQUE, NOT NULL, INDEX | Feed name |
| url | VARCHAR(500) | NOT NULL | RSS feed URL |
| category | VARCHAR(50) | NOT NULL, INDEX | News category |
| is_active | BOOLEAN | DEFAULT TRUE, INDEX | Active status |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Creation timestamp |
| updated_at | DATETIME | ON UPDATE CURRENT_TIMESTAMP | Last update timestamp |

**Indexes**:
- `idx_feed_category`: On category column
- `idx_feed_active`: On is_active column

#### 2. `news_articles`

Stores processed news articles.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| title | VARCHAR(500) | NOT NULL, INDEX | Article title |
| summary | TEXT | | Article summary |
| content | TEXT | | Full article content |
| link | VARCHAR(1000) | NOT NULL, UNIQUE, INDEX | Article URL |
| author | VARCHAR(255) | | Article author |
| published_date | DATETIME | INDEX | Publication date |
| category | VARCHAR(50) | NOT NULL, INDEX | News category |
| source_name | VARCHAR(255) | NOT NULL, INDEX | Source name |
| source_url | VARCHAR(500) | | Source URL |
| image_url | VARCHAR(1000) | | Featured image URL |
| slug | VARCHAR(100) | UNIQUE, INDEX | SEO-friendly slug |
| is_processed | BOOLEAN | DEFAULT FALSE, INDEX | Processing status |
| created_at | DATETIME | DEFAULT CURRENT_TIMESTAMP | Creation timestamp |
| updated_at | DATETIME | ON UPDATE CURRENT_TIMESTAMP | Last update timestamp |

**Indexes**:
- `idx_article_category`: On category column
- `idx_article_source`: On source_name column
- `idx_article_published`: On published_date column
- `idx_article_processed`: On is_processed column
- `idx_article_title`: On title column
- `idx_article_slug`: On slug column

#### 3. `feed_fetch_logs`

Logs RSS feed fetch operations.

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PRIMARY KEY, AUTO_INCREMENT | Unique identifier |
| feed_name | VARCHAR(255) | NOT NULL, INDEX | Feed name |
| fetch_timestamp | DATETIME | DEFAULT CURRENT_TIMESTAMP, INDEX | Fetch timestamp |
| status | VARCHAR(50) | NOT NULL, INDEX | Operation status (success/error/partial) |
| articles_found | INTEGER | DEFAULT 0 | Number of articles found |
| articles_processed | INTEGER | DEFAULT 0 | Number of articles processed |
| error_message | TEXT | | Error message if any |
| execution_time | INTEGER | | Execution time in milliseconds |

**Indexes**:
- `idx_log_feed_name`: On feed_name column
- `idx_log_timestamp`: On fetch_timestamp column
- `idx_log_status`: On status column

### Relationships

- **RSSFeed → NewsArticle**: One-to-many (via source_name)
- **RSSFeed → FeedFetchLog**: One-to-many (via feed_name)

---

## API Documentation

### Base URL

```
http://localhost:8000
```

### Authentication

Currently, no authentication is required. All endpoints are publicly accessible.

### Response Format

All responses are in JSON format.

### Error Responses

Standard error response format:
```json
{
  "detail": "Error message",
  "status_code": 400
}
```

### Endpoints

#### Health Check

**GET** `/api/news/health`

Check API and database health.

**Response**:
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00",
  "database_connected": true,
  "feeds_count": 7,
  "articles_count": 150
}
```

#### Articles

**GET** `/api/news/articles`

Get articles with optional filtering and pagination.

**Query Parameters**:
- `category` (optional): Filter by category (Tech, Global News, Vietnamese News, US News)
- `source` (optional): Filter by source name
- `feeds` (optional): Comma-separated list of feed names
- `page` (optional, default: 1): Page number
- `per_page` (optional, default: 20, max: 100): Articles per page

**Response**:
```json
{
  "articles": [
    {
      "id": 1,
      "title": "Example Article",
      "summary": "Article summary...",
      "content": "Full content...",
      "link": "https://example.com/article",
      "author": "John Doe",
      "published_date": "2024-01-15T10:00:00",
      "category": "Tech",
      "source_name": "TechCrunch",
      "source_url": "https://techcrunch.com",
      "image_url": "https://example.com/image.jpg",
      "slug": "example-article",
      "is_processed": true,
      "created_at": "2024-01-15T10:30:00",
      "updated_at": null
    }
  ],
  "total": 150,
  "page": 1,
  "per_page": 20,
  "total_pages": 8
}
```

**GET** `/api/news/articles/{article_id}`

Get a specific article by ID. Automatically extracts content if missing.

**GET** `/api/news/articles/slug/{slug}`

Get a specific article by slug. Automatically extracts content if missing.

**GET** `/api/news/articles/category/{category}`

Get articles by specific category.

**POST** `/api/news/articles/{article_id}/extract`

Manually trigger content extraction for an article.

#### Feeds

**GET** `/api/news/feeds`

Get all configured RSS feeds.

**Response**:
```json
[
  {
    "id": 1,
    "name": "TechCrunch",
    "url": "https://techcrunch.com/feed/",
    "category": "Tech",
    "is_active": true,
    "created_at": "2024-01-15T10:00:00",
    "updated_at": null
  }
]
```

**GET** `/api/news/feeds/logs`

Get recent RSS fetch logs.

**Query Parameters**:
- `limit` (optional, default: 50, max: 100): Number of logs to return

**GET** `/api/news/feeds/status`

Get status of all RSS feeds.

**POST** `/api/news/feeds/{feed_name}/toggle`

Toggle the active status of a feed.

**DELETE** `/api/news/feeds/delete/{feed_name}`

Delete a feed.

**POST** `/api/news/feeds/add`

Add a new feed.

**Request Body**:
```json
{
  "name": "New Feed",
  "url": "https://example.com/feed.xml",
  "category": "Tech"
}
```

#### Fetch Operations

**POST** `/api/news/fetch`

Manually trigger fetching of all RSS feeds.

**Response**:
```json
{
  "message": "Feed fetching completed",
  "result": {
    "total_feeds": 7,
    "results": [
      {
        "feed_name": "TechCrunch",
        "category": "Tech",
        "status": "success",
        "articles_found": 20,
        "articles_processed": 15,
        "execution_time": 2500
      }
    ]
  }
}
```

**POST** `/api/news/fetch/{feed_name}`

Manually trigger fetching of a specific RSS feed.

#### Search

**GET** `/api/news/search`

Search articles by query with optional filters.

**Query Parameters**:
- `query` (required): Search query string
- `category` (optional, default: "all"): Filter by category
- `time_filter` (optional, default: "24h"): Time filter (24h, 7d, 30d)
- `page` (optional, default: 1): Page number
- `per_page` (optional, default: 20, max: 100): Articles per page

**Response**: Same format as `/api/news/articles`

#### Statistics

**GET** `/api/news/stats`

Get news aggregation statistics.

**Response**:
```json
{
  "total_articles": 150,
  "articles_by_category": {
    "Tech": 50,
    "Global News": 60,
    "Vietnamese News": 40
  },
  "articles_by_source": {
    "TechCrunch": 25,
    "BBC News": 30
  },
  "recent_articles": [...],
  "active_feeds": 7,
  "total_feeds": 7,
  "last_updated": "2024-01-15T10:30:00"
}
```

#### Scheduler Management

**GET** `/api/news/scheduler/status`

Get scheduler status.

**POST** `/api/news/scheduler/start`

Start the scheduler.

**POST** `/api/news/scheduler/stop`

Stop the scheduler.

#### Admin Operations

**DELETE** `/api/news/admin/cleanup/all`

Clean up all data from the database.

**DELETE** `/api/news/admin/cleanup/feed/{feed_name}`

Clean up data for a specific feed.

**DELETE** `/api/news/admin/cleanup/article/{article_id}`

Delete content for a specific article.

---

## Setup & Installation

### Prerequisites

- **Node.js**: 18+ (for frontend)
- **Python**: 3.9+ (for backend)
- **Docker** (optional, for containerized deployment)
- **Git**: For cloning the repository

### Local Development Setup

#### 1. Clone the Repository

```bash
git clone <repository-url>
cd news-4u
```

#### 2. Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Initialize database
python scripts/init_db.py

# Start the server
uvicorn main:app --reload
```

The backend will be available at `http://localhost:8000`

#### 3. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

#### 4. Verify Installation

1. Check backend health: `http://localhost:8000/api/news/health`
2. Check API docs: `http://localhost:8000/docs`
3. Open frontend: `http://localhost:3000`

### Docker Setup

```bash
# Build and start all services
docker-compose up --build

# Run in background
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

This will start:
- PostgreSQL database (port 5432)
- Backend API (port 8000)
- Frontend (port 3000)

---

## Development Guide

### Adding a New RSS Feed

1. **Edit Configuration** (`backend/config/rss_feeds.py`):
   ```python
   RSS_FEEDS = {
       NewsCategory.TECH: [
           # ... existing feeds ...
           RSSFeed(
               name="New Feed Name",
               url="https://example.com/feed.xml",
               category=NewsCategory.TECH,
               is_active=True
           )
       ]
   }
   ```

2. **Initialize Database**:
   ```bash
   python backend/scripts/init_db.py
   ```

3. **Test Feed**:
   ```bash
   curl -X POST http://localhost:8000/api/news/fetch/New%20Feed%20Name
   ```

### Adding a Site-Specific Extractor

1. **Create Extractor Class** (`backend/services/site_extractors.py`):
   ```python
   class NewSiteExtractor(BaseSiteExtractor):
       def extract_content(self, soup: BeautifulSoup, base_url: str) -> Optional[str]:
           primary_selectors = ['div.article-content', 'article']
           return self.extract_with_fallbacks(soup, base_url, primary_selectors)
   ```

2. **Register Extractor**:
   ```python
   # In SiteExtractorManager._register_default_extractors()
   self.extractors.update({
       'newsite.com': NewSiteExtractor(),
   })
   ```

### Database Migrations

When modifying database models:

1. Create migration script in `backend/scripts/`
2. Run migration:
   ```bash
   python backend/scripts/migrate_<description>.py
   ```

### Testing

#### Backend Testing

```bash
# Install test dependencies
pip install pytest pytest-asyncio httpx

# Run tests
pytest
```

#### Frontend Testing

```bash
cd frontend

# Type checking
npm run type-check

# Linting
npm run lint
```

### Code Formatting

#### Backend

```bash
# Install formatting tools
pip install black isort

# Format code
black .
isort .
```

#### Frontend

```bash
cd frontend

# Format with Prettier (if configured)
npm run format
```

### Debugging

#### Backend Debugging

1. **Enable Debug Logging**:
   ```python
   import logging
   logging.basicConfig(level=logging.DEBUG)
   ```

2. **Check Logs**:
   - Console output for application logs
   - Database logs in `feed_fetch_logs` table

#### Frontend Debugging

1. **Browser DevTools**: Use React DevTools and Network tab
2. **Console Logs**: Check browser console for errors
3. **API Calls**: Monitor network requests in DevTools

---

## Deployment

### Backend Deployment

#### Option 1: Docker

```bash
cd backend
docker build -t news-4u-backend .
docker run -p 8000:8000 news-4u-backend
```

#### Option 2: Direct Deployment

1. Set environment variables:
   ```bash
   export DATABASE_URL="postgresql://user:pass@host:5432/news_4u"
   ```

2. Install dependencies and run:
   ```bash
   pip install -r requirements.txt
   uvicorn main:app --host 0.0.0.0 --port 8000
   ```

### Frontend Deployment

#### Option 1: Vercel (Recommended)

1. Connect repository to Vercel
2. Set environment variable: `NEXT_PUBLIC_API_URL`
3. Deploy

#### Option 2: Docker

```bash
cd frontend
docker build -t news-4u-frontend .
docker run -p 3000:3000 -e NEXT_PUBLIC_API_URL=http://api-url news-4u-frontend
```

#### Option 3: Static Export

```bash
cd frontend
npm run build
# Serve the out/ directory
```

### Production Considerations

1. **Database**: Use PostgreSQL instead of SQLite
2. **Environment Variables**: Set proper API URLs
3. **CORS**: Configure CORS for production domains
4. **Scheduler**: Ensure scheduler is running in production
5. **Monitoring**: Set up logging and monitoring
6. **Backup**: Regular database backups
7. **Security**: Add authentication if needed
8. **Rate Limiting**: Implement rate limiting for API

---

## Troubleshooting

### Common Issues

#### 1. Database Locked Error

**Problem**: SQLite database is locked.

**Solution**:
- Ensure no other process is accessing the database
- Check if SQLite shell is open
- Restart the application

#### 2. RSS Feed Fetch Failures

**Problem**: Feeds fail to fetch.

**Solution**:
- Check internet connectivity
- Verify RSS feed URLs are accessible
- Check `feed_fetch_logs` table for error details
- Some sites may block automated requests

#### 3. Content Extraction Fails

**Problem**: Article content not extracted.

**Solution**:
- Check article URL is accessible
- Verify site extractor exists for the domain
- Check logs for extraction errors
- Some sites may block content extraction

#### 4. Import Errors

**Problem**: Module import errors.

**Solution**:
- Ensure virtual environment is activated
- Reinstall dependencies: `pip install -r requirements.txt`
- Check Python path

#### 5. Frontend API Errors

**Problem**: Frontend can't connect to backend.

**Solution**:
- Verify `NEXT_PUBLIC_API_URL` is set correctly
- Check backend is running
- Verify CORS configuration
- Check network connectivity

### Getting Help

1. Check logs in console output
2. Review `feed_fetch_logs` table
3. Check API documentation at `/docs`
4. Review error messages in browser console

---

## Future Enhancements

### Potential Features

1. **User Authentication**: User accounts and preferences
2. **Bookmarking**: Save favorite articles
3. **Notifications**: Notify users of new articles
4. **Email Digest**: Daily/weekly email summaries
5. **RSS Feed Export**: Export articles as RSS feed
6. **Advanced Analytics**: Detailed statistics and insights
7. **Multi-language Support**: Support for multiple languages
8. **Mobile App**: Native mobile applications
9. **Social Sharing**: Share articles on social media
10. **Comments**: User comments on articles

### Technical Improvements

1. **Caching**: Implement Redis caching
2. **Search Engine**: Full-text search with Elasticsearch
3. **CDN**: Content delivery network for static assets
4. **Load Balancing**: Multiple backend instances
5. **Message Queue**: Async task processing with Celery
6. **Monitoring**: Application performance monitoring
7. **Testing**: Comprehensive test coverage
8. **CI/CD**: Continuous integration and deployment

---

## License

[Specify your license here]

---

## Contributing

[Add contribution guidelines if applicable]

---

## Contact

[Add contact information if applicable]

---

**Last Updated**: January 2024

**Version**: 1.0.0

