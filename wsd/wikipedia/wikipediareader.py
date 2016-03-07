import threading
import multiprocessing
import Queue
import logging
import xml.sax
import nltk.data
from nltk.tokenize import *
import re


class WikipediaReader(threading.Thread):
    '''allows to read a wikipedia xml dump file and extract articles
    '''

    '''constructor

        @param path the path to the wikiepdia dump file
        @param queue the queue to which articles shall be read as dictionary with the following fields:
            'type': 'article' or 'redirect'
            'id': the id of the article (not present for redirects)
            'title': the title of the article or redirect
            'text': the actual text (not present for redirects or when the extraction of text was disabled)
            'target': the name of the article to which the redirect points to (not present for articles)
        @param extract_text boolean whether text shall also be extracted (defaults to true)
    '''

    def __init__(self, path, queue, extract_text=True):
        threading.Thread.__init__(self)
        # multiprocessing.Process.__init__(self)
        self._reader = WikipediaArticleReader(queue, extract_text)
        self._path = path

    def run(self):
        xml.sax.parse(self._path, self._reader)
        logging.info('Finished parsing file "%s"' % self._path)

    def articles_parsed(self):
        '''returns the number of articles already parsed
        '''
        return self._reader.articles_parsed()


class WikipediaArticleReader(xml.sax.handler.ContentHandler):
    '''A SAX content handler that reads articles from a wikipedia file
    '''

    '''constructor

       @param queue the queue to which articles shall be read
       @param extract_text boolean whether text shall also be extracted (defaults to true)
    '''

    def __init__(self, queue, extract_text=True):
        self._queue = queue
        self._reset()
        self._current_tag = u''
        self._article_counter = 0
        self._id_done = False
        self._rev_id_done = False
        self._ns_done = False
        self._extract_text = extract_text

    def _reset(self):
        self._id_done = False
        self._rev_id_done = False
        self._ns_done = False
        self._item = {
            'type': u'article',
            'id': u'',
            'rev_id': u'',
            'ns': u'',
            'title': u'',
            'text': u'',
            'target': u''
        }

    def articles_parsed(self):
        return self._article_counter

    def startElement(self, name, attrs):
        # print name
        self._current_tag = name
        if self._current_tag == 'redirect':
            self._item['type'] = u'redirect'
            if not 'title' in attrs.getNames():
                logging.warning('Attribute "title" not in redirect tag of article "%s"'
                                % (self._item['title'].encode('ascii', 'ignore')))
            self._item['target'] = attrs.getValue('title')

            #if self._current_tag == 'template':
            #    self._item['type'] = u'template'
            #if not 'title' in attrs.getNames():
            #    logging.warning('Attribute "title" not in redirect tag of article "%s"'
            #        % (self._item['title'].encode('ascii', 'ignore')))
            #self._item['target'] = attrs.getValue('title')

    def characters(self, content):
        if self._current_tag == 'title':
            self._item['title'] += content
            # print self._item['title']
        elif self._current_tag == 'id' and not self._id_done:
            self._item['id'] += content
        elif self._current_tag == 'id' and self._id_done and not self._rev_id_done:
            self._item['rev_id'] += content
        elif self._current_tag == 'ns' and not self._ns_done:
            self._item['ns'] += content
        elif self._current_tag == 'text' and self._extract_text and not self._item['type'] == u'redirect':
            self._item['text'] += content

    def endElement(self, name):
        self._current_tag = u''
        if name == 'id' and not self._id_done:
            self._id_done = True
        elif name == 'id' and self._id_done and not self._rev_id_done:
            self._rev_id_done = True
        elif name == 'ns':
            self._ns_done = True
        elif name == 'page':
            self._article_counter += 1
            # consider just articles and templates pages and do not handle empty titles

            if len(self._item['title']) > 0 and (long(self._item['ns']) == 0 ):
                try:
                    self._item['id'] = long(self._item['id'])
                    self._queue.put(self._item)
                except ValueError:
                    logging.error('Article "%s" could not be parsed, as %s is not a valid integer id'
                                  % (
                    self._item['title'].encode('ascii', 'ignore'), self._item['id'].encode('ascii', 'ignore')))
            # log progress
            if self._article_counter % 100 == 0:
                logging.info('%d articles parsed' % (self._article_counter))

            # reset article
            self._reset()

