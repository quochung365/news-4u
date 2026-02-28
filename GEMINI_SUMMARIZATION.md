# Gemini AI Summarization Feature

This feature uses Google's Gemini API (free tier) to automatically generate concise summaries of news article content.

## Features

- ✅ Single article summarization
- ✅ Batch summarization (up to 20 articles)
- ✅ Automatic HTML cleaning
- ✅ Free tier compatible (gemini-2.0-flash-exp model)
- ✅ Smart token management (truncates long articles)

## Setup

### 1. Get Your Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key

### 2. Add API Key to Environment

Add your Gemini API key to your `.env` file:

```bash
# In backend/.env
GEMINI_API_KEY=your_actual_api_key_here
```

**Note:** The key is already configured in your [backend/.env](backend/.env:7) file. Just replace `your_gemini_api_key_here` with your real API key.

### 3. Restart the Application

If running locally:
```bash
cd backend
# Activate your virtual environment if using one
python main.py
```

If running with Docker:
```bash
# No rebuild needed! Just restart
docker-compose restart backend

# Or if you prefer:
docker-compose down
docker-compose up -d
```

If deployed on Linode:
```bash
ssh news4u@your-linode-ip
cd news-4u

# Edit .env file
nano backend/.env

# Update GEMINI_API_KEY, then restart
docker-compose -f docker-compose.prod.yml restart backend
```

## API Endpoints

### Summarize Single Article

**Endpoint:** `POST /api/news/articles/{article_id}/summarize`

**Example:**
```bash
curl -X POST "http://localhost:8000/api/news/articles/123/summarize"
```

**Response:**
```json
{
  "id": 123,
  "title": "Article Title",
  "summary": "AI-generated concise summary...",
  "content": "Full article content...",
  ...
}
```

### Summarize Multiple Articles (Batch)

**Endpoint:** `POST /api/news/articles/summarize/batch`

**Example:**
```bash
curl -X POST "http://localhost:8000/api/news/articles/summarize/batch" \
  -H "Content-Type: application/json" \
  -d '{"article_ids": [123, 124, 125]}'
```

**Request Body:**
```json
{
  "article_ids": [123, 124, 125]
}
```

**Response:**
```json
{
  "status": "success",
  "total_requested": 3,
  "total_found": 3,
  "total_summarized": 3,
  "summaries": {
    "123": "Summary for article 123...",
    "124": "Summary for article 124...",
    "125": "Summary for article 125..."
  }
}
```

## Usage Workflow

### Typical Flow:

1. **Fetch articles** from RSS feeds:
   ```bash
   POST /api/news/fetch
   ```

2. **Get article list**:
   ```bash
   GET /api/news/articles?page=1&per_page=20
   ```

3. **Extract full content** (if needed):
   ```bash
   POST /api/news/articles/{article_id}/extract
   ```

4. **Generate AI summary**:
   ```bash
   POST /api/news/articles/{article_id}/summarize
   ```

### Frontend Integration

```typescript
// Fetch article with summary
async function getArticleWithSummary(articleId: number) {
  // Get the article
  const article = await fetch(`/api/news/articles/${articleId}`);
  const data = await article.json();

  // If no content, extract it first
  if (!data.content) {
    await fetch(`/api/news/articles/${articleId}/extract`, {
      method: 'POST'
    });
  }

  // Generate summary
  const response = await fetch(`/api/news/articles/${articleId}/summarize`, {
    method: 'POST'
  });

  return await response.json();
}

// Batch summarize
async function summarizeArticles(articleIds: number[]) {
  const response = await fetch('/api/news/articles/summarize/batch', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ article_ids: articleIds })
  });

  return await response.json();
}
```

## API Rate Limits (Gemini Free Tier)

- **Requests per minute (RPM):** 15
- **Requests per day (RPD):** 1,500
- **Tokens per minute (TPM):** 1,000,000

For batch operations, space out requests to avoid rate limits.

## Troubleshooting

### Error: "Article has no content to summarize"

**Solution:** Extract content first:
```bash
POST /api/news/articles/{article_id}/extract
```

### Error: "GEMINI_API_KEY not configured"

**Solution:**
1. Check your [backend/.env](backend/.env) file
2. Make sure `GEMINI_API_KEY` is set
3. Restart the backend service

### Error: "Rate limit exceeded"

**Solution:**
- You've hit Gemini's free tier rate limit
- Wait 60 seconds and try again
- For batch operations, reduce the number of articles per request

### Slow Response Times

**Expected:** 2-5 seconds per article (depends on content length)

**If slower:**
- Check your internet connection
- Verify Gemini API status: https://status.cloud.google.com/

## Cost

✅ **FREE** - Uses Gemini's free tier (gemini-2.0-flash-exp model)

No credit card required for the free tier.

## Files Modified

- [backend/services/llm/gemini.py](backend/services/llm/gemini.py) - Gemini API integration
- [backend/routers/news.py](backend/routers/news.py) - Added summarization endpoints
- [backend/services/llm/__init__.py](backend/services/llm/__init__.py) - Module initialization

## Testing

Test the API using the interactive docs:
- Local: http://localhost:8000/docs
- Production: https://api.hqtran.com/docs (or your domain)

Look for the new endpoints under the "Article" section.
