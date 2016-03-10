/*The script created the clickstream table and pupulates it. the delete statement removes the first record in the table corresponding to the first line in the tsv file that despribes the coloumns in the file.*/
CREATE TABLE `clickstream` (`prev_id` bigint(20) NOT NULL, `curr_id` bigint(20) NOT NULL, `counts` bigint(20) NOT NULL, `prev_title` varchar(2000) COLLATE utf8_bin NOT NULL, `curr_title` varchar(2000) COLLATE utf8_bin NOT NULL, `link_type` varchar(255) COLLATE utf8_bin NOT NULL, `id` bigint(20) NOT NULL AUTO_INCREMENT, PRIMARY KEY (`id`) ) ENGINE=InnoDB  DEFAULT CHARSET=utf8 AUTO_INCREMENT=0;
LOAD DATA LOCAL INFILE '/path/to/2015_02_clickstream.tsv' INTO TABLE `clickstream` COLUMNS TERMINATED BY '\t' LINES TERMINATED BY '\n';
DELETE FROM clickstream WHERE id=1;

ALTER TABLE clickstream ADD INDEX (prev_id);
ALTER TABLE clickstream ADD INDEX (curr_id);
ALTER TABLE clickstream ADD INDEX (counts);
ALTER TABLE clickstream ADD INDEX (prev_title);
ALTER TABLE clickstream ADD INDEX (curr_title);
ALTER TABLE clickstream ADD INDEX (link_type);

