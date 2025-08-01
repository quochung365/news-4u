"""
Database models for the news aggregation system.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, Index
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()


class RSSFeed(Base):
    """Model for storing RSS feed information."""
    __tablename__ = "rss_feeds"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True, index=True)
    url = Column(String(500), nullable=False)
    category = Column(String(50), nullable=False, index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    

    
    __table_args__ = (
        Index('idx_feed_category', 'category'),
        Index('idx_feed_active', 'is_active'),
    )





class NewsArticle(Base):
    """Model for storing processed news articles."""
    __tablename__ = "news_articles"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String(500), nullable=False, index=True)
    summary = Column(Text)
    content = Column(Text)
    link = Column(String(1000), nullable=False, unique=True, index=True)
    author = Column(String(255))
    published_date = Column(DateTime(timezone=True))
    category = Column(String(50), nullable=False, index=True)
    source_name = Column(String(255), nullable=False, index=True)
    source_url = Column(String(500))
    image_url = Column(String(1000))
    slug = Column(String(100), unique=True, index=True)
    is_processed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    __table_args__ = (
        Index('idx_article_category', 'category'),
        Index('idx_article_source', 'source_name'),
        Index('idx_article_published', 'published_date'),
        Index('idx_article_processed', 'is_processed'),
        Index('idx_article_title', 'title'),
        Index('idx_article_slug', 'slug'),
    )


class FeedFetchLog(Base):
    """Model for logging RSS feed fetch operations."""
    __tablename__ = "feed_fetch_logs"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    feed_name = Column(String(255), nullable=False, index=True)
    fetch_timestamp = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(50), nullable=False)  # success, error, partial
    articles_found = Column(Integer, default=0)
    articles_processed = Column(Integer, default=0)
    error_message = Column(Text)
    execution_time = Column(Integer)  # in milliseconds
    
    __table_args__ = (
        Index('idx_log_feed_name', 'feed_name'),
        Index('idx_log_timestamp', 'fetch_timestamp'),
        Index('idx_log_status', 'status'),
    ) 