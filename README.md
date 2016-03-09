### WIKILINKS ###
Wikilinks is a parsing framework for Wikipedia. It is based on the code of the wikiwsd project by Paul Laufer
(xml dump processing) and code by Daniel Lamprecht for parsing HTML text. The framework extracts the id, revision, and
title of an article form the xml dump. Redirects are resoleved using the xml dump. The corresponding HTML for each article is then crawled from the wikipedia api and processed.
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

### Requermnents ###


### Building the database ###




### About ###

### TODOS ###
- extract link from cations of figures.
- extract the text of the link.

### License ###
This project is published under the MIT License.

