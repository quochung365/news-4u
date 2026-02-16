# News 4U API Reference

Comprehensive API documentation for the News 4U RSS aggregator backend.

## Base URL

```
http://localhost:8000
```

For production, replace with your deployed API URL.

## Interactive Documentation

Once the backend is running, you can access interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Authentication

Currently, the API does not require authentication. Admin endpoints should be protected in production.

## Response Format

All responses are in JSON format with appropriate HTTP status codes.

### Success Response
```json
{
  "data": { /* response data */ }
}
```

### Error Response
```json
{
  "detail": "Error message",
  "status_code": 400
}
```

## Status Codes

- `200 OK` - Successful request
- `201 Created` - Resource created successfully
- `400 Bad Request` - Invalid request parameters
- `404 Not Found` - Resource not found
- `500 Internal Server Error` - Server error

---

## Endpoints

### Health Check

#### `GET /api/news/health`

Check API and database health status.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00",
  "database_connected": true,
  "feeds_count": 10,
  "articles_count": 500
}
```

---

## Feed Management

### Get All Feeds

#### `GET /api/news/feeds`

Get list of all configured RSS feeds.

**Response:**
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

### Get Feed Status

#### `GET /api/news/feeds/status`

Get status of all feeds with latest fetch information.

**Response:**
```json
{
  "feeds": [
    {
      "name": "TechCrunch",
      "category": "Tech",
      "is_active": true,
      "last_fetch": "2024-01-15T10:30:00",
      "last_status": "success",
      "articles_processed": 20
    }
  ]
}
```

### Get Feed Logs

#### `GET /api/news/feeds/logs`

Get recent feed fetch logs.

**Query Parameters:**
- `limit` (optional, default: 50, max: 100) - Number of logs to return

**Response:**
```json
[
  {
    "id": 1,
    "feed_id": 1,
    "fetch_timestamp": "2024-01-15T10:30:00",
    "status": "success",
    "articles_found": 20,
    "articles_processed": 15,
    "error_message": null,
    "execution_time_ms": 2500
  }
]
```

### Add Feed

#### `POST /api/news/feeds/add`

Add a new RSS feed.

**Request Body:**
```json
{
  "name": "Example Feed",
  "url": "https://example.com/feed",
  "category": "Tech"
}
```

**Response:**
```json
{
  "message": "Feed Example Feed added successfully"
}
```

### Toggle Feed Status

#### `POST /api/news/feeds/{feed_name}/toggle`

Toggle the active status of a feed.

**Path Parameters:**
- `feed_name` (string) - Name of the feed

**Response:**
```json
{
  "status": "success",
  "feed_name": "TechCrunch",
  "is_active": false,
  "message": "Feed 'TechCrunch' deactivated"
}
```

### Delete Feed

#### `DELETE /api/news/feeds/delete/{feed_name}`

Delete a feed from the database.

**Path Parameters:**
- `feed_name` (string) - Name of the feed

**Response:**
```json
{
  "status": "success",
  "message": "Feed 'TechCrunch' deleted successfully"
}
```

### Fetch All Feeds

#### `POST /api/news/fetch`

Manually trigger fetching of all active RSS feeds.

**Response:**
```json
{
  "message": "Feed fetching completed",
  "result": {
    "status": "success",
    "feeds_processed": 7,
    "total_articles_found": 140,
    "total_articles_processed": 120,
    "results": [
      {
        "feed_name": "TechCrunch",
        "status": "success",
        "articles_found": 20,
        "articles_processed": 15,
        "execution_time": 2500
      }
    ]
  }
}
```

### Fetch Specific Feed

#### `POST /api/news/fetch/{feed_name}`

Manually trigger fetching of a specific RSS feed.

**Path Parameters:**
- `feed_name` (string) - Name of the feed

**Response:**
```json
{
  "feed_name": "TechCrunch",
  "status": "success",
  "articles_found": 20,
  "articles_processed": 15,
  "execution_time": 2500
}
```

---

## Article Management

### Get Articles

#### `GET /api/news/articles`

Get articles with optional filtering and pagination.

**Query Parameters:**
- `category` (optional) - Filter by category
- `source` (optional) - Filter by source name
- `feeds` (optional) - Comma-separated list of feed names
- `page` (optional, default: 1) - Page number
- `per_page` (optional, default: 20, max: 100) - Articles per page

**Examples:**
```
GET /api/news/articles?page=1&per_page=20
GET /api/news/articles?category=Tech&page=1
GET /api/news/articles?feeds=TechCrunch,BBC
```

**Response:**
```json
{
  "articles": [
    {
      "id": 1,
      "title": "Example Article",
      "summary": "Article summary...",
      "content": "Full article content...",
      "link": "https://example.com/article",
      "author": "John Doe",
      "published_date": "2024-01-15T10:00:00",
      "category": "Tech",
      "feed_name": "TechCrunch",
      "image_url": "https://example.com/image.jpg",
      "slug": "example-article",
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

### Get Article by ID

#### `GET /api/news/articles/{article_id}`

Get a specific article by ID. Automatically extracts content if missing.

**Path Parameters:**
- `article_id` (integer) - Article ID

**Response:**
```json
{
  "id": 1,
  "title": "Example Article",
  "summary": "Article summary...",
  "content": "Full article content...",
  "link": "https://example.com/article",
  "author": "John Doe",
  "published_date": "2024-01-15T10:00:00",
  "category": "Tech",
  "feed_name": "TechCrunch",
  "image_url": "https://example.com/image.jpg",
  "slug": "example-article",
  "created_at": "2024-01-15T10:30:00",
  "updated_at": null
}
```

### Get Article by Slug

#### `GET /api/news/articles/slug/{slug}`

Get a specific article by slug. Automatically extracts content if missing.

**Path Parameters:**
- `slug` (string) - Article slug

**Response:** Same as Get Article by ID

### Get Articles by Category

#### `GET /api/news/articles/category/{category}`

Get articles by specific category.

**Path Parameters:**
- `category` (string) - Category name (Tech, Global News, Vietnamese News, US News)

**Query Parameters:**
- `page` (optional, default: 1) - Page number
- `per_page` (optional, default: 20, max: 100) - Articles per page

**Response:** Same format as Get Articles

### Extract Article Content

#### `POST /api/news/articles/{article_id}/extract`

Manually trigger content extraction for a specific article.

**Path Parameters:**
- `article_id` (integer) - Article ID

**Response:**
```json
{
  "id": 1,
  "title": "Example Article",
  "content": "Extracted content...",
  "image_url": "https://example.com/image.jpg",
  // ... other fields
}
```

---

## Search

### Search Articles

#### `GET /api/news/search`

Search articles with optional filters.

**Query Parameters:**
- `query` (required) - Search query string
- `category` (optional, default: "all") - Filter by category
- `time_filter` (optional, default: "24h") - Time filter (24h, 7d, 30d, all)
- `page` (optional, default: 1) - Page number
- `per_page` (optional, default: 20, max: 100) - Articles per page

**Examples:**
```
GET /api/news/search?query=AI&category=Tech&time_filter=7d
GET /api/news/search?query=bitcoin&page=2
```

**Response:** Same format as Get Articles

---

## Statistics

### Get Statistics

#### `GET /api/news/stats`

Get aggregated statistics about articles and feeds.

**Response:**
```json
{
  "total_articles": 500,
  "articles_by_category": {
    "Tech": 200,
    "Global News": 150,
    "Vietnamese News": 100,
    "US News": 50
  },
  "articles_by_source": {
    "1": 50,
    "2": 40
  },
  "recent_articles": [
    {
      "id": 1,
      "title": "Recent Article",
      "source_name": 1,
      "created_at": "2024-01-15T10:30:00"
    }
  ],
  "active_feeds": 7,
  "total_feeds": 10,
  "last_updated": "2024-01-15T10:30:00"
}
```

---

## Scheduler Management

### Get Scheduler Status

#### `GET /api/news/scheduler/status`

Get the current status of the background scheduler.

**Response:**
```json
{
  "status": "running"
}
```

### Start Scheduler

#### `POST /api/news/scheduler/start`

Start the background scheduler.

**Response:**
```json
{
  "message": "Scheduler started"
}
```

### Stop Scheduler

#### `POST /api/news/scheduler/stop`

Stop the background scheduler.

**Response:**
```json
{
  "message": "Scheduler stopped"
}
```

---

## Admin Operations

⚠️ **Warning**: These endpoints should be protected with authentication in production.

### Cleanup All Data

#### `DELETE /api/news/admin/cleanup/all`

Delete all articles and fetch logs from the database.

**Response:**
```json
{
  "message": "All data cleaned up successfully"
}
```

### Cleanup Feed Data

#### `DELETE /api/news/admin/cleanup/feed/{feed_name}`

Delete all data for a specific feed.

**Path Parameters:**
- `feed_name` (string) - Name of the feed

**Response:**
```json
{
  "message": "Data for feed 'TechCrunch' cleaned up successfully"
}
```

### Delete Article Content

#### `DELETE /api/news/admin/cleanup/article/{article_id}`

Delete content for a specific article (keeps metadata).

**Path Parameters:**
- `article_id` (integer) - Article ID

**Response:**
```json
{
  "message": "Content for article 1 deleted successfully"
}
```

---

## Data Models

### NewsArticle

```typescript
{
  id: number;
  title: string;
  summary?: string;
  content?: string;
  link: string;
  author?: string;
  published_date?: string; // ISO 8601 format
  category: string;
  feed_id?: number;
  image_url?: string;
  slug?: string;
  created_at: string; // ISO 8601 format
  updated_at?: string; // ISO 8601 format
  feed_name?: string;
}
```

### RSSFeed

```typescript
{
  id: number;
  name: string;
  url: string;
  category: string;
  description?: string;
  is_active: boolean;
  created_at: string; // ISO 8601 format
  updated_at?: string; // ISO 8601 format
}
```

### FeedFetchLog

```typescript
{
  id: number;
  feed_id: number;
  fetch_timestamp: string; // ISO 8601 format
  status: string; // "success", "error", "partial"
  articles_found: number;
  articles_processed: number;
  error_message?: string;
  execution_time_ms?: number;
}
```

---

## Error Codes

### Common Errors

#### 400 Bad Request
```json
{
  "detail": "Invalid request parameters",
  "status_code": 400
}
```

**Causes:**
- Missing required parameters
- Invalid parameter values
- Malformed request body

#### 404 Not Found
```json
{
  "detail": "Article not found or feed is inactive",
  "status_code": 404
}
```

**Causes:**
- Resource doesn't exist
- Feed is inactive
- Invalid ID or slug

#### 500 Internal Server Error
```json
{
  "detail": "Internal server error",
  "error": "Detailed error message"
}
```

**Causes:**
- Database connection issues
- Unhandled exceptions
- External service failures

---

## Rate Limiting

Currently, no rate limiting is implemented. Consider adding rate limiting in production to prevent abuse.

---

## CORS Configuration

The API allows requests from:
- `http://localhost:3000`
- `http://127.0.0.1:3000`
- `https://news-4u.onrender.com`
- `https://news-4u.vercel.app`
- `http://news.localhost`
- `http://news.hqtran.com`

To add more origins, update the CORS middleware configuration in [main.py](backend/main.py).

---

## Webhooks

Currently, no webhooks are implemented. This section is reserved for future webhook functionality.

---

## Best Practices

### Pagination
Always use pagination for large datasets:
```
GET /api/news/articles?page=1&per_page=20
```

### Feed Filtering
When filtering by multiple feeds, use comma-separated values:
```
GET /api/news/articles?feeds=TechCrunch,BBC,CNBC
```

### Error Handling
Always check the `status_code` in responses and handle errors appropriately:
```javascript
try {
  const response = await fetch('/api/news/articles');
  if (!response.ok) {
    const error = await response.json();
    console.error('API Error:', error.detail);
  }
} catch (error) {
  console.error('Network Error:', error);
}
```

### Caching
Consider implementing client-side caching for frequently accessed endpoints like feeds list and article metadata.

---

## SDK Examples

### JavaScript/TypeScript

```typescript
// Using Axios
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
  timeout: 10000
});

// Get articles
const getArticles = async (page = 1, perPage = 20) => {
  const response = await api.get('/api/news/articles', {
    params: { page, per_page: perPage }
  });
  return response.data;
};

// Search articles
const searchArticles = async (query, timeFilter = '24h') => {
  const response = await api.get('/api/news/search', {
    params: { query, time_filter: timeFilter }
  });
  return response.data;
};

// Fetch feeds
const fetchFeeds = async () => {
  await api.post('/api/news/fetch');
};
```

### Python

```python
import requests

BASE_URL = "http://localhost:8000"

# Get articles
def get_articles(page=1, per_page=20):
    response = requests.get(
        f"{BASE_URL}/api/news/articles",
        params={"page": page, "per_page": per_page}
    )
    return response.json()

# Search articles
def search_articles(query, time_filter="24h"):
    response = requests.get(
        f"{BASE_URL}/api/news/search",
        params={"query": query, "time_filter": time_filter}
    )
    return response.json()

# Fetch feeds
def fetch_feeds():
    response = requests.post(f"{BASE_URL}/api/news/fetch")
    return response.json()
```

---

## Version History

- **v1.0.0** (2024-01-15) - Initial API release
  - Basic CRUD operations for articles and feeds
  - Search functionality
  - Scheduler management
  - Admin operations

---

## Support

For issues or questions:
1. Check [backend/README.md](backend/README.md)
2. View interactive docs at http://localhost:8000/docs
3. Open an issue on GitHub (if applicable)
