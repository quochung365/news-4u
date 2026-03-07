"""
Scheduler service for managing cronjobs.
"""

import asyncio
import logging
from datetime import datetime
from typing import Optional
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session
from sqlalchemy import text

from database import get_db
from services.rss import RSSService
from services.extractors import Extractor
from models import NewsArticle
from config.settings import settings

logger = logging.getLogger(__name__)


class SchedulerService:
    """Service for managing scheduled tasks."""
    
    def __init__(self):
        self.scheduler = AsyncIOScheduler()
        self.is_running = False
    
    def start(self):
        print("---- Starting Scheduler Service ----")
        """Start the scheduler."""
        if not self.is_running:
            self.scheduler.start()
            self.is_running = True
            logger.info("Scheduler started")
            # Add the cronjobs
            self._add_feed_fetching_job()
            self._add_content_extraction_job()
    
    def stop(self):
        """Stop the scheduler."""
        if self.is_running:
            self.scheduler.shutdown()
            self.is_running = False
            logger.info("Scheduler stopped")
    
    def _add_feed_fetching_job(self):
        """Add the job to fetch all feeds every 5 minutes."""
        self.scheduler.add_job(
            func=self._fetch_all_feeds_job,
            trigger=CronTrigger(minute="*/15"),  # Every 15 minutes
            id="fetch_all_feeds",
            name="Fetch all RSS feeds",
            replace_existing=True,
            max_instances=1
        )
        logger.info("Added feed fetching job (every 15 minutes)")
    
    def _add_content_extraction_job(self):
        """Add the job to extract content every minute."""
        self.scheduler.add_job(
            func=self._extract_content_job,
            trigger=CronTrigger(minute="*"),  # Every minute
            id="extract_content",
            name="Extract article content",
            replace_existing=True,
            max_instances=1
        )
        logger.info("Added content extraction job (every minute)")
    
    async def _fetch_all_feeds_job(self):
        """Job to fetch all RSS feeds."""
        logger.info("---- Starting scheduled feed fetching job ----")
        try:
            db = next(get_db())
            service = RSSService(db)
            result = await service.fetch_all_feeds()
            logger.info(f"Feed fetching completed: {result}")
        except Exception as e:
            logger.error(f"Error in feed fetching job: {e}")
        finally:
            if 'db' in locals():
                db.close()
    
    async def _extract_content_job(self):
        """Job to extract content for articles that haven't been extracted."""
        logger.info("---- Starting scheduled content extraction job ----")
        try:
            db = next(get_db())

            sql = text("""
                SELECT * FROM news_articles n
                JOIN rss_feeds r ON n.feed_id = r.id
                WHERE n.content IS NULL OR n.content = '' OR n.content = 'None'
                AND n.retry_count < :max_retry
                AND n.link IS NOT NULL
                AND r.skip_extraction = FALSE
                ORDER BY n.created_at DESC
                LIMIT 30
            """)

            params = {"max_retry": settings.ARTICLE_EXTRACTION_MAX_RETRY}
            articles_without_content = db.execute(sql, params).all()
            
            if not articles_without_content:
                logger.info("No articles found that need content extraction")
                return
            
            logger.info(f"Found {len(articles_without_content)} articles that need content extraction")

            extractor = Extractor()
            extracted_count = 0

            for article in articles_without_content:
                try:
                    #  convert article from string to NewsArticle object
                    article = NewsArticle(**article._mapping)
                    print(f"Extracting content for article {article.id}: {article.title}")
                    logger.info(f"Extracting content for article {article.id}: {article.title}")
                    content, extracted_image_url = extractor.extract(article)
                    
                    if content:
                        setattr(article, 'content', content)
                        extracted_count += 1
                        logger.info(f"Successfully extracted content for article {article.id}")
                    
                    if extracted_image_url and not getattr(article, 'image_url', None):
                        setattr(article, 'image_url', extracted_image_url)
                        logger.info(f"Updated image URL for article {article.id}")
                    
                    # Update the article timestamp
                    setattr(article, 'updated_at', datetime.now())
                    
                except Exception as e:
                    logger.error(f"Scheduler: Error extracting content for article {article.id}: {e}")
                    continue
            
            # Commit all changes
            db.commit()
            logger.info(f"Content extraction job completed. Extracted content for {extracted_count} articles")
            
        except Exception as e:
            logger.error(f"Error in content extraction job: {e}")
        finally:
            if 'db' in locals():
                db.close()
    
    def get_job_status(self) -> dict:
        """Get the status of all scheduled jobs."""
        jobs = []
        for job in self.scheduler.get_jobs():
            jobs.append({
                "id": job.id,
                "name": job.name,
                "next_run_time": job.next_run_time.isoformat() if job.next_run_time else None,
                "trigger": str(job.trigger)
            })
        
        return {
            "scheduler_running": self.is_running,
            "jobs": jobs
        }


# Global scheduler instance
scheduler_service = SchedulerService() 