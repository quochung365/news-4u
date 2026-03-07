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

from database import get_db
from services.rss import RSSService
from services.extractors import Extractor
from models import NewsArticle, RSSFeed
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


            # Issue: 
            # SQL query on lines 92-95 uses SELECT * with a JOIN between news_articles and rss_feeds tables. This means article._mapping contains columns from both tables, including duplicate column names like:

            # id (from both news_articles and rss_feeds) ← This causes the error
            # category (from both tables)
            # created_at (from both tables)
            # updated_at (from both tables)
            # When you try to do NewsArticle(**article._mapping) on line 119, SQLAlchemy sees multiple values for the same parameter and throws the error.

            # sql = text("""
            #     SELECT * FROM news_articles n
            #     JOIN rss_feeds r ON n.feed_id = r.id
            #     WHERE n.content IS NULL OR n.content = '' OR n.content = 'None'
            #     AND n.retry_count < :max_retry
            #     AND n.link IS NOT NULL
            #     AND r.skip_extraction = FALSE
            #     ORDER BY n.created_at DESC
            #     LIMIT 30
            # """)

            # params = {"max_retry": settings.ARTICLE_EXTRACTION_MAX_RETRY}
            # articles_without_content = db.execute(sql, params).all()
           
            # Query using ORM instead of raw SQL
            articles_without_content = (
                db.query(NewsArticle)
                .join(NewsArticle.feed)
                .filter(
                    (NewsArticle.content == None) |
                    (NewsArticle.content == '') |
                    (NewsArticle.content == 'None')
                )
                .filter(NewsArticle.retry_count < settings.ARTICLE_EXTRACTION_MAX_RETRY)
                .filter(NewsArticle.link != None)
                .filter(RSSFeed.skip_extraction == False)
                .order_by(NewsArticle.created_at.desc())
                .limit(30)
                .all()
            )

            if not articles_without_content:
                logger.info("No articles found that need content extraction")
                return

            logger.info(f"Found {len(articles_without_content)} articles that need content extraction")

            extractor = Extractor()
            extracted_count = 0

            # Process fewer articles at a time to avoid blocking for too long
            batch_size = 5
            for i, article in enumerate(articles_without_content[:batch_size]):
                try:
                    print(f"Extracting content for article {article.id}: {article.title}")
                    logger.info(f"Extracting content for article {article.id}: {article.title}")

                    # Run blocking extraction in a thread pool to avoid blocking the event loop
                    content, extracted_image_url = await asyncio.to_thread(
                        extractor.extract, article
                    )

                    if content:
                        setattr(article, 'content', content)
                        extracted_count += 1
                        logger.info(f"Successfully extracted content for article {article.id}")

                    if extracted_image_url and not getattr(article, 'image_url', None):
                        setattr(article, 'image_url', extracted_image_url)
                        logger.info(f"Updated image URL for article {article.id}")

                    # Update the article timestamp
                    setattr(article, 'updated_at', datetime.now())

                    # Yield control back to event loop between articles
                    await asyncio.sleep(0.1)

                except Exception as e:
                    logger.error(f"Scheduler: Error extracting content for article {article.id}: {e}")
                    continue

            # Commit all changes
            db.commit()
            logger.info(f"Content extraction job completed. Extracted content for {extracted_count}/{len(articles_without_content)} articles")
            
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