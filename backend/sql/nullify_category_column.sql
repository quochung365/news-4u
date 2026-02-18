-- Migration: Nullify category column in news_articles table
-- Date: 2026-02-15
-- Description: Sets all category values to NULL as category is no longer needed

-- Update all existing articles to have NULL category
UPDATE news_articles
SET category = NULL;

-- Verify the update
SELECT COUNT(*) as total_articles,
       COUNT(category) as articles_with_category
FROM news_articles;
