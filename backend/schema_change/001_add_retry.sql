alter table news_articles
add column retry_count integer not null default 0;