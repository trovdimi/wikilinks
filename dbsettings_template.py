'''This file contains the database connection settings to be used and 
   needs to be altered accordingly
'''

DATABASE_HOST = 'localhost'
DATABASE_USER = 'wikilinks'
DATABASE_PASSWORD = 'wikilinks'
DATABASE_NAME = 'wikilinks'
WIKI_DUMP_XML_FILE = '/path/to/dump/xml' # e.g, enwiki-20150304-pages-articles.xml
MEDIAWIKI_API_ENDPOINT = 'https://en.wikipedia.org/api/rest_v1/page/html/'# see: https://en.wikipedia.org/api/rest_v1/?doc
STATIC_HTML_DUMP_ARTICLES_DIR = '/path/to/wikipedia_html_dump/articles/'
STATIC_HTML_DUMP_ERRORS_DIR = '/path/to/wikipedia_html_dump/errors/'
EMAIL = 'change@mymail.me' # please change to your mail. See mediawiki api policy: https://en.wikipedia.org/api/rest_v1/?doc

