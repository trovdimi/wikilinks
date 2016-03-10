'''This file contains the database connection and other settings to be used and
   needs to be altered accordingly
'''

DATABASE_HOST = 'localhost'
DATABASE_USER = 'root'
DATABASE_PASSWORD = 'gesis#2015'
DATABASE_NAME = 'wikilinks'
WIKI_DUMP_XML_FILE = '/home/ddimitrov/data/enwiki20150304_plus_clickstream/enwiki-20150304-pages-articles.xml'
MEDIAWIKI_API_ENDPOINT = 'https://en.wikipedia.org/api/rest_v1/page/html/'# see: https://en.wikipedia.org/api/rest_v1/?doc
STATIC_HTML_DUMP_ARTICLES_DIR = '/home/ddimitrov/wikipedia_html_dump/articles/'
STATIC_HTML_DUMP_ERRORS_DIR = '/home/ddimitrov/wikipedia_html_dump/error/'
EMAIL = 'dimitar.dimitrov@gesis.org'

