#!/usr/bin/env python3
"""
Database initialization script for SQLite.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from database import init_db, get_db, engine
from models.database import RSSFeed, NewsArticle, FeedFetchLog
from config.rss_feeds import get_all_feeds
from sqlalchemy import text


def ensure_slug_column():
    """Ensure slug column exists in news_articles table."""
    try:
        with engine.connect() as conn:
            # First check if table exists
            result = conn.execute(text("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='news_articles'
            """))
            table_exists = result.fetchone() is not None
            
            if not table_exists:
                # Table doesn't exist yet, init_db() will create it with the correct schema
                return
            
            # Check if slug column already exists
            result = conn.execute(text("""
                SELECT COUNT(*) FROM pragma_table_info('news_articles') 
                WHERE name = 'slug'
            """))
            count = result.scalar()
            column_exists = count is not None and count > 0
            
            if not column_exists:
                print("Adding slug column to news_articles table...")
                conn.execute(text("""
                    ALTER TABLE news_articles 
                    ADD COLUMN slug VARCHAR(100)
                """))
                
                # Create unique index on slug column
                conn.execute(text("""
                    CREATE UNIQUE INDEX IF NOT EXISTS idx_article_slug_unique ON news_articles(slug)
                """))
                conn.commit()
                print("✓ Slug column added to news_articles table")
            else:
                print("✓ Slug column already exists")
    except Exception as e:
        print(f"Warning: Could not check/add slug column: {e}")


def main():
    """Initialize database and load initial data."""
    print("Initializing News 4U SQLite database...")
    
    # Initialize database tables
    init_db()
    print("✓ Database tables created")
    
    # Ensure slug column exists (for existing databases)
    ensure_slug_column()

    # Delete all RSSFeeds
    db = next(get_db())
    db.query(RSSFeed).delete()
    db.commit()
    print("✓ All RSSFeeds deleted")
    
    # Load RSS feeds
    db = next(get_db())
    try:
        feeds = get_all_feeds()
        loaded_count = 0
        
        for feed in feeds:
            existing = db.query(RSSFeed).filter(RSSFeed.name == feed.name).first()
            if not existing:
                db_feed = RSSFeed(
                    name=feed.name,
                    url=feed.url,
                    category=feed.category.value,
                    is_active=feed.is_active
                )
                db.add(db_feed)
                loaded_count += 1
        
        db.commit()
        if loaded_count > 0:
            print(f"✓ Loaded {loaded_count} new RSS feeds")
        else:
            print("✓ All RSS feeds already exist in database (no changes made)")
        
        # Show database status
        total_feeds = db.query(RSSFeed).count()
        total_articles = db.query(NewsArticle).count()
    
        total_logs = db.query(FeedFetchLog).count()
        
        print(f"\nDatabase Status:")
        print(f"  RSS Feeds: {total_feeds}")
        print(f"  Articles: {total_articles}")
        print(f"  Fetch Logs: {total_logs}")
        
    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
        sys.exit(1)
    finally:
        db.close()
    
    print("\n✓ SQLite database initialization completed successfully!")


if __name__ == "__main__":
    main() 