BEGIN;
ALTER TABLE news_articles
ADD COLUMN feed_id INTEGER;

ALTER TABLE news_articles
ADD CONSTRAINT fk_news_articles_feed
FOREIGN KEY (feed_id)
REFERENCES rss_feeds(id)
ON DELETE SET NULL;


ALTER TABLE feed_fetch_logs
ADD COLUMN feed_id INTEGER;

ALTER TABLE feed_fetch_logs
ADD CONSTRAINT fk_feed_fetch_logs_feed
FOREIGN KEY (feed_id)
REFERENCES rss_feeds(id)
ON DELETE CASCADE;


ALTER TABLE feed_fetch_logs
RENAME COLUMN execution_time TO execution_time_ms;


ALTER TABLE news_articles
DROP COLUMN source_name,
DROP COLUMN source_url;


CREATE INDEX ix_news_articles_feed_id ON news_articles(feed_id);
CREATE INDEX ix_feed_fetch_logs_feed_id ON feed_fetch_logs(feed_id);
CREATE INDEX ix_news_articles_published_date ON news_articles(published_date);


ALTER TABLE rss_feeds
ALTER COLUMN updated_at SET DEFAULT now();

ALTER TABLE news_articles
ALTER COLUMN updated_at SET DEFAULT now();


UPDATE feed_fetch_logs l
SET feed_id = f.id
FROM rss_feeds f
WHERE l.feed_name = f.name;

COMMIT;