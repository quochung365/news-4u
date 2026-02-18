# Category Removal & Code Cleanup Summary

**Date**: 2026-02-15

## Overview

Removed the redundant category field and consolidated duplicated content extraction logic across the codebase. The category column remains in the database for backward compatibility but is set to NULL for all articles.

---

## Changes Made

### 1. Database Migration

**File Created**: [backend/sql/nullify_category_column.sql](backend/sql/nullify_category_column.sql)

Sets all category values to NULL in the `news_articles` table.

```sql
UPDATE news_articles
SET category = NULL;
```

**To apply**: Run the SQL file against your database:
```bash
psql -h localhost -U your_user -d news4u_db -f backend/sql/nullify_category_column.sql
```

---

### 2. Removed Redundant `extract_article_content` Wrapper

**File**: [backend/services/rss.py](backend/services/rss.py#L175-180)

**Before:**
```python
async def extract_article_content(self, article: NewsArticle) -> tuple[Optional[str], Optional[str]]:
    """Extract full article content from URL using multiple strategies."""
    extractor = Extractor()
    return extractor.extract(article)
```

**After**: Method removed entirely

**Reason**: This was a thin wrapper that just instantiated `Extractor()` and called its `extract()` method. All callers now use `Extractor` directly, eliminating unnecessary indirection.

---

### 3. Consolidated Content Extraction Logic

**File**: [backend/services/scheduler_service.py](backend/services/scheduler_service.py#L85-147)

**Before:**
```python
service = RSSService(db)
content, extracted_image_url = await service.extract_article_content(article)
```

**After:**
```python
extractor = Extractor()
content, extracted_image_url = extractor.extract(article)
```

**Changes**:
- Removed unnecessary `RSSService` instantiation in `_extract_content_job`
- Now uses `Extractor` directly (no `await` needed since `Extractor.extract()` is synchronous)
- Added import: `from services.extractors import Extractor`

---

### 4. Updated Article API Endpoints

**File**: [backend/routers/news.py](backend/routers/news.py)

Updated three endpoint functions to use `Extractor` directly:

**Affected Functions**:
- `get_article()` - Line 241-297
- `get_article_by_slug()` - Line 300-355
- `extract_article_content()` - Line 453-492

**Before**:
```python
service = RSSService(db)
content, extracted_image_url = await service.extract_article_content(article)
```

**After**:
```python
extractor = Extractor()
content, extracted_image_url = extractor.extract(article)
```

**Changes**:
- Removed `await` keyword (method is synchronous)
- Added import: `from services.extractors import Extractor`
- Removed unused import: `from config.rss_feeds import NewsCategory`

---

### 5. Removed Category Assignment in Article Processing

**File**: [backend/services/rss.py](backend/services/rss.py#L354-375)

**Method**: `_build_article_object()`

**Before:**
```python
raw_data = {
    "title": title,
    "summary": self._extract_summary(entry),
    "link": link,
    "author": self._safe_get_string(entry, 'author'),
    "published_date": self._extract_published_date(entry),
    "category": feed.category,  # ← Removed this line
    "source_name": feed.name,
    "image_url": self._extract_image(entry),
    "slug": get_or_build_slug(link, title),
    "feed_id": feed.id,
}
```

**After:**
```python
raw_data = {
    "title": title,
    "summary": self._extract_summary(entry),
    "link": link,
    "author": self._safe_get_string(entry, 'author'),
    "published_date": self._extract_published_date(entry),
    "source_name": feed.name,
    "image_url": self._extract_image(entry),
    "slug": get_or_build_slug(link, title),
    "feed_id": feed.id,
}
```

---

### 6. Removed `get_articles_by_category()` Method

**File**: [backend/services/rss.py](backend/services/rss.py#L211-221)

**Method Removed**:
```python
def get_articles_by_category(self, category: str, limit: int = 50, offset: int = 0) -> List[NewsArticle]:
    """Get articles by category with pagination."""
    if self.db is None:
        return []
    return self.db.query(NewsArticle).filter(
        NewsArticle.category == category.value
    ).order_by(
        NewsArticle.published_date.desc()
    ).offset(offset).limit(limit).all()
```

**Reason**: Category field is deprecated, so this method is no longer needed.

---

### 7. Updated Category API Endpoint

**File**: [backend/routers/news.py](backend/routers/news.py#L358-390)

**Endpoint**: `GET /api/news/articles/category/{category}`

**Changes**:
- Updated docstring: "Note: Category field is deprecated and will return no results."
- Changed `NewsArticle.category == category.value` to `NewsArticle.category == category`
- This endpoint will return empty results since all categories are now NULL

**Note**: Consider deprecating or removing this endpoint in a future release.

---

### 8. Updated Schemas

**File**: [backend/schemas.py](backend/schemas.py)

**Before**:
```python
from config.rss_feeds import NewsCategory

class RSSFeedBase(BaseModel):
    name: str
    url: str
    category: Optional[NewsCategory] = None

class RSSFeedUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    category: Optional[NewsCategory] = None
    is_active: Optional[bool] = None
```

**After**:
```python
# NewsCategory import removed

class RSSFeedBase(BaseModel):
    name: str
    url: str
    category: Optional[str] = None

class RSSFeedUpdate(BaseModel):
    name: Optional[str] = None
    url: Optional[str] = None
    category: Optional[str] = None
    is_active: Optional[bool] = None
```

**Changes**:
- Removed `NewsCategory` enum import
- Changed `category` field type from `Optional[NewsCategory]` to `Optional[str]`
- `NewsArticleBase.category` was already `Optional[str]`, no changes needed

---

### 9. Updated RSS Feeds Configuration

**File**: [backend/config/rss_feeds.py](backend/config/rss_feeds.py)

**Major Changes**:

1. **Converted `RSSFeed` from `NamedTuple` to `@dataclass`**:
```python
# Before
class RSSFeed(NamedTuple):
    name: str
    url: str
    category: NewsCategory
    is_active: bool = True

# After
@dataclass
class RSSFeed:
    name: str
    url: str
    category: Optional[str] = None
    is_active: bool = True
```

2. **Marked `NewsCategory` enum as deprecated**:
```python
class NewsCategory(str, Enum):
    """Deprecated: Category field is no longer used."""
    TECH = "Tech"
    GLOBAL_NEWS = "Global News"
    VIETNAMESE_NEWS = "Vietnamese News"
    US_NEWS = "US News"
```

3. **Simplified `RSS_FEEDS` structure**:
```python
# Before
RSS_FEEDS: Dict[NewsCategory, List[RSSFeed]] = {
    NewsCategory.VIETNAMESE_NEWS: [
        RSSFeed(name="Vnexpress", url="...", category=NewsCategory.VIETNAMESE_NEWS, is_active=True),
        # ...
    ],
    # ...
}

# After
RSS_FEEDS: List[RSSFeed] = [
    RSSFeed(name="Vnexpress", url="https://vnexpress.net/rss/the-gioi.rss", is_active=True),
    RSSFeed(name="Tuoitre", url="https://tuoitre.vn/rss/the-gioi.rss", is_active=True),
    RSSFeed(name="TechCrunch", url="https://techcrunch.com/feed/", is_active=True),
    # ... (11 feeds total, no categories)
]
```

---

## Summary of Files Modified

| File | Changes |
|------|---------|
| [backend/sql/nullify_category_column.sql](backend/sql/nullify_category_column.sql) | ✨ NEW - SQL migration to nullify category column |
| [backend/services/rss.py](backend/services/rss.py) | Removed `extract_article_content()` method, removed `get_articles_by_category()` method, removed category assignment in `_build_article_object()`, removed `Extractor` import |
| [backend/services/scheduler_service.py](backend/services/scheduler_service.py) | Updated `_extract_content_job()` to use `Extractor` directly, added `Extractor` import |
| [backend/routers/news.py](backend/routers/news.py) | Updated 3 endpoint functions to use `Extractor` directly, updated `get_articles_by_category()` endpoint, removed `NewsCategory` import, added `Extractor` import |
| [backend/schemas.py](backend/schemas.py) | Removed `NewsCategory` import, changed `category` type from `NewsCategory` to `str` in feed schemas |
| [backend/config/rss_feeds.py](backend/config/rss_feeds.py) | Converted `RSSFeed` to dataclass, made `category` optional, deprecated `NewsCategory` enum, simplified `RSS_FEEDS` structure |

---

## Key Benefits

### 1. Reduced Code Duplication
- **Before**: Content extraction logic was duplicated between `RSSService.extract_article_content()` and `_extract_content_job`
- **After**: All code uses `Extractor` directly - single source of truth

### 2. Cleaner Architecture
- Removed unnecessary wrapper method that added no value
- Reduced coupling between `RSSService` and `Extractor`
- Simpler call chain: `Extractor().extract()` instead of `RSSService().extract_article_content()` which internally called `Extractor().extract()`

### 3. Simplified Data Model
- Category field is deprecated but kept for backward compatibility
- Removed enum constraint, making the system more flexible
- Flattened RSS_FEEDS structure from nested dict to simple list

### 4. Improved Performance (Minor)
- Removed one unnecessary async/await layer
- One less object instantiation (`RSSService`) in scheduler job

---

## Migration Steps

To apply these changes to your running system:

1. **Pull the latest code**:
```bash
git pull origin <branch>
```

2. **Apply the database migration**:
```bash
cd backend
psql -h localhost -U your_user -d news4u_db -f sql/nullify_category_column.sql
```

3. **Restart the backend server**:
```bash
# Stop the current server
# Then restart
uvicorn main:app --reload
```

4. **Verify**:
- Check that articles are still being fetched
- Check that content extraction is still working
- Verify that search and filtering work correctly

---

## Breaking Changes

### API Changes

**None** - The API endpoints remain the same. Category fields are still present in responses but will be `null`.

### Deprecated Endpoints

- `GET /api/news/articles/category/{category}` - Will return empty results since all categories are NULL
- Consider removing this endpoint in a future release

### Configuration Changes

If you have custom scripts that use `RSS_FEEDS` from `config/rss_feeds.py`:
- **Before**: `RSS_FEEDS` was a `Dict[NewsCategory, List[RSSFeed]]`
- **After**: `RSS_FEEDS` is a `List[RSSFeed]`

**Migration**:
```python
# Before
for category, feeds in RSS_FEEDS.items():
    for feed in feeds:
        print(feed.name, feed.category)

# After
for feed in RSS_FEEDS:
    print(feed.name, feed.category)  # category will be None
```

---

## Testing Checklist

- [ ] Run database migration
- [ ] Restart backend server
- [ ] Verify feed fetching works (`POST /api/news/fetch`)
- [ ] Verify article retrieval works (`GET /api/news/articles`)
- [ ] Verify content extraction works (`POST /api/news/articles/{id}/extract`)
- [ ] Check scheduler is running (`GET /api/news/scheduler/status`)
- [ ] Monitor logs for any errors
- [ ] Verify search functionality works
- [ ] Check that new articles are created without category

---

## Future Considerations

### Potential Improvements

1. **Remove Category Column** (Breaking Change):
   - After confirming all systems work correctly, consider dropping the `category` column entirely from the database schema
   - Would require a database migration and updates to models/schemas

2. **Remove Deprecated Endpoint**:
   - Remove `GET /api/news/articles/category/{category}` endpoint
   - Update API documentation

3. **Remove NewsCategory Enum**:
   - Once all references are removed, delete the `NewsCategory` enum entirely from `config/rss_feeds.py`

---

## Questions or Issues?

If you encounter any issues after applying these changes:

1. Check the application logs for errors
2. Verify the database migration was applied successfully
3. Ensure all dependencies are up to date
4. Review the changes in this document

For questions, please refer to the main project documentation or create an issue.

---

**Total Changes**: 6 files modified, 1 file created
**Lines of Code Removed**: ~60 lines
**Lines of Code Added**: ~30 lines
**Net Reduction**: ~30 lines of code
