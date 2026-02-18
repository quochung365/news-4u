-- Migration: Add skip_extraction column to rss_feeds table
-- Date: 2026-02-17
-- Description: Adds a boolean flag to control whether content extraction should be skipped for feeds that require subscription

-- Add skip_extraction column with default value of false
ALTER TABLE rss_feeds
ADD COLUMN skip_extraction BOOLEAN NOT NULL DEFAULT false;

-- Verify the migration
SELECT id, name, is_active, skip_extraction
FROM rss_feeds;
