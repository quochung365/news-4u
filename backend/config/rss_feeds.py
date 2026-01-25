"""
RSS Feeds Configuration
"""

from typing import Dict, List, NamedTuple
from enum import Enum
from pydantic import BaseModel
from database import SessionLocal


class NewsCategory(str, Enum):
    TECH = "Tech"
    GLOBAL_NEWS = "Global News"
    VIETNAMESE_NEWS = "Vietnamese News"
    US_NEWS = "US News"

class RSSFeed(NamedTuple):
    name: str
    url: str
    category: NewsCategory
    is_active: bool = True

# RSS Feeds Configuration - SEED DATA ONLY
# This dictionary is used by scripts/init_db.py to populate the database with initial feeds.
# After seeding, the database becomes the source of truth. Changes here won't affect runtime.
RSS_FEEDS: Dict[NewsCategory, List[RSSFeed]] = {
    NewsCategory.VIETNAMESE_NEWS: [
        RSSFeed(
            name="Vnexpress",
            url="https://vnexpress.net/rss/the-gioi.rss",
            category=NewsCategory.VIETNAMESE_NEWS,
            is_active=True
        ),
        RSSFeed(
            name="Tuoitre",
            url="https://tuoitre.vn/rss/the-gioi.rss",
            category=NewsCategory.VIETNAMESE_NEWS,
            is_active=True
        )
    ],
    NewsCategory.TECH: [
        RSSFeed(
            name="TechCrunch",
            url="https://techcrunch.com/feed/",
            category=NewsCategory.TECH,
            is_active=True
        ),
        RSSFeed(
            name="The Verge",
            url="https://www.theverge.com/rss/index.xml",
            category=NewsCategory.TECH,
            is_active=True
        ),
        RSSFeed(
            name="Engadget",
            url="https://www.engadget.com/rss.xml",
            category=NewsCategory.TECH,
            is_active=True
        )
    ],
    NewsCategory.US_NEWS: [
        RSSFeed(
            name="CNBC",
            url="https://www.cnbc.com/id/100003114/device/rss/rss.html",
            category=NewsCategory.US_NEWS,
            is_active=True
        ),
        RSSFeed(
            name="NBC News",
            url="https://feeds.nbcnews.com/nbcnews/public/news",
            category=NewsCategory.US_NEWS,
            is_active=True
        ),
        RSSFeed(
            name= "ABC News",
            url="https://abcnews.go.com/abcnews/usheadlines",
            category=NewsCategory.US_NEWS,
            is_active=True
        ),
    ],

    NewsCategory.GLOBAL_NEWS: [
        RSSFeed(
            name="BBC News",
            url="https://feeds.bbci.co.uk/news/rss.xml",
            category=NewsCategory.GLOBAL_NEWS,
            is_active=True
        ),
        RSSFeed(
            name="CNBC Global",
            url="https://www.cnbc.com/id/100727362/device/rss/rss.html",
            category=NewsCategory.GLOBAL_NEWS,
            is_active=True
        ),
        RSSFeed(
            name="CBSNews",
            url="https://www.cbsnews.com/latest/rss/world",
            category=NewsCategory.GLOBAL_NEWS,
            is_active=True
        ),
    ]    
}

def seed_data():
    db = SessionLocal()
    try:
        # 1. Check if data already exists to prevent duplicates
        existing_feed = db.query()
        existing_user = db.query(models.User).filter(models.User.email == "admin@example.com").first()
        
        if not existing_user:
            print("Seeding initial data...")
            new_user = models.User(
                email="admin@example.com",
                hashed_password="hashed_password_here" # Use real hashing in prod
            )
            db.add(new_user)
            db.commit()
            print("Seed successful!")
        else:
            print("Data already exists, skipping seed.")
            
    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()