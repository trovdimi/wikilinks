# WIKILINKS #
Wikilinks is a parsing framework for Wikipedia written in Python. It is based on the code of the wikiwsd project by Paul Laufer
(XML dump processing) and code by Daniel Lamprecht for parsing HTML text. The framework is intended to extract different link features (e.g., network topological, visual) from Wikipedia in order to study human navigation. 
It can be used in combination with the clickstream [dataset](http://ewulczyn.github.io/Wikipedia_Clickstream_Getting_Started/) by Ellery Wulczyn, Dario Taraborelli from Wikimedia. 
The corresponding Wikipedia XML dump can be found [here](https://archive.org/details/enwiki-20150304) for more recent dumps can be found [here](https://en.wikipedia.org/wiki/Wikipedia:Database_download).
 
The framework extracts the id, revision id, and title (`id`, `rev_id`, `title) of an article form the XML dump. Redirects are resoleved using the XML dump. The corresponding HTML for each article is then crawled from the wikipedia api and processed.
For each link (`source_article_id`,`target_article_id` pair in the `links` table) in the zero namespace of wikipedia it extracts then the following information:
- `target_position_in_text target` link's position in text 
- `target_position_in_text_only` target link's position in text only, all links in tables are ignored
- `target_position_in_section`  position in section
- `target_position_in_section_in_text_only`  target link's position in section only, all links in tables of the section are ignored
- `section_name` the name of the section
- `section_number` the number of the section
- `target_position_in_table` position of the target link in the table
- `table_number` the number of the table
- `table_css_class` the cascading style sheed class of the table (can be used to classify the tables, i.e., infobox, navibox, etc.)
- `table_css_style` further styling of the table, extraced from the style element of the table tag (can be used to classify the tables, i.e., infobox, navibox, etc.)
- `target_x_coord_1920_1080` the x coorodinate of the visual position of the left upper corner of the target link for resoluion 1920x1080
- `target_y_coord_1920_1080` the y coorodinate of the visual position of the left upper corner of the target link for resoluion 1920x1080
- `target_position_in_paragraphs` the position of the target link in all paragraphs
- `target_position_in_paragraph` the position of the target link in a paragraph
- `paragraph_number` the number of the paragraph

For each article in the `article` table we also extract the corresponding web page length of the rendered html and store it in the
field `page_length_1920_1080` of the table `page_length`. The page lenght can be used in different ways, e.g., normalization.

### Requirements ###
MySQL Database 5, PyQt4, Xvfb


### Building the database ###
    CREATE DATABASE `wikilinks` DEFAULT CHARACTER SET utf8 DEFAULT COLLATE utf8_bin;
    GRANT ALL ON `wikilinks`.* TO `wikilinks`@`localhost` IDENTIFIED BY 'wikilinks';
    GRANT ALL ON `wikilinks`.* TO `wikilinks`@`%` IDENTIFIED BY 'wikilinks';


We use binary collation for comparing string, i.e., article titles - [see stackoverflow entry](http://stackoverflow.com/questions/5526334/what-effects-does-using-a-binary-collation-have).


Please copy the dbsettings_template.py file to dbsettings.py and change the settings accordingly to your database setup.

### Modules descrioption and use ##

# builder.py #
After creating the databese this should be the first script to execute.
The interactive `builder.py` script should be rather self-explanatory. It allows one to:

1. Create the basic database structure (create tables: articles and rederects )
2. Create the reference entries for articles by parsing the Wikipedia dump files and resolving redirects

# crawler.py#
The `crawler.py`  uses the `id` and `rev_id` of an article in the 'articles' table to crawl corresponding the HTML file. 
This process takes around 2 days with  20 threads. The size of the zipped dump is around 60GB. 


# startlinkinserter.py #
The `startlinkinserter.py` script creates and populates the tables: `links`, `page_length`. Xfvb screen has to be available at DISPLAY 1, before it can be run since it extracts visual postions of the links. 
You will need a lot of RAM for this process and it can take some days to finish.

# tableclassinserter.py #
The `tableclassinserter.py` script creates and populates the table `table_css_class`. 

# heatmaps.py#
The `heatmaps.py` script uses the clickstream data and the link data to create heatmaps showing in which regions on screan links are places and consumed.

 
### TODOS ###
- extract link from cations of figures.
- extract the text of the link.
- configurabel number of threads for the crawler, and for the parsers

### License ###
This project is published under the MIT License.

