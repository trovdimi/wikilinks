# -*- coding: utf-8 -*-
'''
This file contains the code which allows to easily
build and prepare the database used for the disambiguation library

Author: Paul Laufer
Date: Oct 2013

'''

import os
import time
import logging
import Queue
from multiprocessing import JoinableQueue
from wsd.database import MySQLDatabase
from wsd.wikipedia import WikipediaReader
from wsd.build import ArticleInserter
from consoleapp import ConsoleApp
from dbsettings import *

class BuilderApp(ConsoleApp):
    '''The EvaluationApp class is a console application to facilitate
       the building process
    '''

    def __init__(self):
        pass

    def run(self):
        self.print_title('This is the interactive building program')
        self.create_tmp_if_not_exists()

        choice = self.read_choice('Would you like to', [
            'create the database structure', 
            'extract articles and redirects from the wikipedia dump file'
            ])

        # setup logging
        LOGGING_FORMAT = '%(levelname)s:\t%(asctime)-15s %(message)s'
        LOGGING_PATH = self.read_path('Please enter the path of the logging file [.log]', default='./tmp/build-%d.log' % (choice[0]+1), must_exist=False)
        logging.basicConfig(filename=LOGGING_PATH, level=logging.DEBUG, format=LOGGING_FORMAT, filemode='w')

        if choice[0] == 0:
            self._create_structure()
        if choice[0] == 1:
            self._extract_articles()


    def _create_structure(self):

        # measure time
        start = time.clock()

        # creating structure
        db = MySQLDatabase(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
        db.build()

        seconds = round (time.clock() - start)
        logging.info('Finished after %02d:%02d minutes' % (seconds / 60, seconds % 60))
        print 'Finished after %02d:%02d minutes' % (seconds / 60, seconds % 60)

    def _extract_articles(self):


        INPUT_FILE = WIKI_DUMP_XML_FILE #self.read_path('Please enter the path of the wiki dump file [.xml]')
        #INPUT_FILE = "/home/ddimitrov/wikiwsd/data/training.xml"#self.read_path('Please enter the path of the wiki dump file [.xml]')
        MAX_ARTICLES_IN_QUEUE = 200#self.read_number('How many articles should be kept in the memory at any time at most?', 200, 20, 1000)
        NUM_THREADS = 1#self.read_number('How many threads shall be used to write to the database?', 20, 1, 50)
        CONTINUE = True#self.read_yes_no('This process might take several days to finish.\nDo you want to continue?')

        if CONTINUE:
            # measure time
            start = time.clock()

            # connect to database and create article queue
            db = MySQLDatabase(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
            queue = Queue.Queue(maxsize=MAX_ARTICLES_IN_QUEUE)

            # create reader and threads
            reader = WikipediaReader(INPUT_FILE, queue, extract_text=False)
            threads = []
            for i in range(0, NUM_THREADS):
                inserter = ArticleInserter(queue, db.get_build_view())
                threads.append(inserter)

            # start reader
            reader.start()

            # start insert threads
            for thread in threads:
                thread.start()

            # wait for reading thread, queue and inserters to be done
            reader.join()
            queue.join()
            for thread in threads:
                thread.end()
            for thread in threads:
                thread.join()

            seconds = round (time.clock() - start)
            print 'Finished after %02d:%02d minutes' % (seconds / 60, seconds % 60)

        else:
            print 'Aborting...'


if __name__ == '__main__':
    runner = BuilderApp()
    runner.run()
