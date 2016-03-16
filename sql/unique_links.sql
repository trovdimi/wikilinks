CREATE TABLE unique_links AS (SELECT DISTINCT source_article_id, target_article_id FROM links);
ALTER TABLE unique_links ADD PRIMARY KEY (source_article_id, target_article_id);
ALTER TABLE unique_links ADD INDEX (target_article_id);
