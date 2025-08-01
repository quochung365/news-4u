"""
Main FastAPI application for the News 4U RSS aggregator.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import uvicorn

from database import init_db, get_db
from routers import news
from config.rss_feeds import get_all_feeds
from services.scheduler_service import scheduler_service
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""

    logger.info("Starting News 4U RSS Aggregator...")
    init_db()
    logger.info("Database initialized")
    
    from models.database import RSSFeed
    db = next(get_db())
    try:
        feeds = get_all_feeds()
        for feed in feeds:
            existing = db.query(RSSFeed).filter(RSSFeed.name == feed.name).first()
            if not existing:
                db_feed = RSSFeed(
                    name=feed.name,
                    url=feed.url,
                    category=feed.category.value
                )
                db.add(db_feed)
        db.commit()
        logger.info(f"Loaded {len(feeds)} RSS feeds")
    finally:
        db.close()
    
    # Start the scheduler
    scheduler_service.start()
    logger.info("Scheduler started with cronjobs")
    
    yield
    
    # Stop the scheduler
    scheduler_service.stop()
    logger.info("Scheduler stopped")
    logger.info("Shutting down News 4U RSS Aggregator...")


app = FastAPI(
    title="News 4U RSS Aggregator",
    description="A professional news aggregation platform that fetches and categorizes news from popular RSS feeds.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000", 
        "http://127.0.0.1:3000",
        "https://news-4u.onrender.com",
        "https://news-4u.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(news.router)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "News 4U RSS Aggregator API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/news/health"
    }


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Global HTTP exception handler."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Global exception handler."""
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "error": str(exc)
        }
    )


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    ) 