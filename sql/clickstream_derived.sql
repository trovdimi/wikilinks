/*This scirpt creates the clickstream_derived table containing all links that could be mapped and classify them according to a classification schema more suitalbe for studing navigation.
The scripts also creates a table with the missmatched transistion, useful for ,i.e., reporting purposes in a paper .
The script have to be executed after the unique_links and clickstream tables are pupulated*/
CREATE TABLE `clickstream_derived` LIKE `clickstream`;
INSERT `clickstream_derived` SELECT * FROM `clickstream`;
ALTER TABLE `clickstream_derived` ADD `link_type_derived` VARCHAR(255);

/*ALTER TABLE clickstream_derived ADD INDEX (prev_id);
ALTER TABLE clickstream_derived ADD INDEX (curr_id);
ALTER TABLE clickstream_derived ADD INDEX (counts);
ALTER TABLE clickstream_derived ADD INDEX (prev_title);
ALTER TABLE clickstream_derived ADD INDEX (curr_title);
ALTER TABLE clickstream_derived ADD INDEX (link_type);*/

UPDATE clickstream_derived SET link_type_derived="entry-se" WHERE prev_title ="other-google" OR prev_title LIKE "other-bing" OR prev_title LIKE "other-yahoo";
UPDATE clickstream_derived SET link_type_derived="entry-sm"  WHERE prev_title LIKE "other-twitter" OR prev_title LIKE "other-facebook";
UPDATE clickstream_derived SET link_type_derived="wikipedia-entrypoint"  WHERE prev_title LIKE "other-wikipedia";
UPDATE clickstream_derived SET link_type_derived ="wikimedia-entrypoint"  WHERE prev_title LIKE "other-internal";
UPDATE clickstream_derived SET link_type_derived="noreferrer" WHERE prev_title LIKE "other-empty";
UPDATE clickstream_derived SET link_type_derived="other"  WHERE prev_title LIKE "other-other";

/*select count(*) from clickstream_derived w WHERE exists (SELECT 1 FROM unique_links l WHERE  w.prev_id=l.source_article_id AND w.curr_id=l.target_article_id) and w.link_type_derived is not null;
 Should be 0 thus we can execute the next update - internal-link*/
UPDATE clickstream_derived w SET w.link_type_derived="internal-link" WHERE EXISTS (SELECT 1 FROM unique_links l WHERE  w.prev_id=l.source_article_id AND w.curr_id=l.target_article_id);

/*select distinct(link_type_derived) from clickstream_derived w  WHERE exists (SELECT 1 FROM unique_links l WHERE  w.prev_id=l.source_article_id AND w.curr_id=l.target_article_id) and w.prev_id = w.curr_id and w.link_type_derived is not null;
should be internal-link thus we can execute the next update - internal-self-loop */
UPDATE clickstream_derived w SET w.link_type_derived="internal-self-loop"  WHERE EXISTS (SELECT 1 FROM unique_links l WHERE  w.prev_id=l.source_article_id AND w.curr_id=l.target_article_id) AND w.prev_id = w.curr_id;

/*select count(*) from  clickstream_derived w WHERE not exists (SELECT 1 FROM unique_links l WHERE  w.prev_id=l.source_article_id AND w.curr_id=l.target_article_id) AND w.prev_id!=0 and w.curr_id!=0 and w.link_type_derived is not null;
 Should be 0 thus we can execute the next updates - internal-teleportation,internal-nonexistent */
UPDATE clickstream_derived w SET w.link_type_derived="internal-teleportation" WHERE NOT EXISTS (SELECT 1 FROM unique_links l WHERE  w.prev_id=l.source_article_id AND w.curr_id=l.target_article_id) AND w.prev_id!=0 AND w.curr_id!=0;
UPDATE clickstream_derived w SET w.link_type_derived = "internal-nonexistent" WHERE NOT EXISTS (SELECT 1 FROM articles a WHERE a.id =w.curr_id);

/*select count(*) from clickstream_derived where link_type_derived is null;
Should be 0*/

ALTER TABLE clickstream_derived ADD INDEX (link_type_derived);


/*Now we clean up the clickstream_derived table --- we delete all transitions that clould not be matched*/
CREATE TABLE mismatched_transtions AS (SELECT * FROM clickstream_derived w WHERE (NOT EXISTS (SELECT 1 FROM articles a WHERE a.id =w.curr_id) AND w.curr_id !=0) OR (NOT EXISTS (SELECT 1 FROM articles aa WHERE aa.id=w.prev_id) AND w.prev_id!=0));

ALTER TABLE mismatched_transtions ADD PRIMARY KEY (id);

DELETE FROM clickstream_derived WHERE id IN (SELECT id FROM mismatched_transtions);