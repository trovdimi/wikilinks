from scipy.stats._discrete_distns import zipf_gen
import requests
import threading
import json
import codecs
import time
import os
import urllib
import errno
import zipfile
from wsd.database import MySQLDatabase
from dbsettings import *
__author__ = 'dimitrovdr'

#MEDIAWIKI_API_ENDPOINT = 'https://en.wikipedia.org/w/api.php?action=parse&format=json&prop=text&oldid=' #see:
#MEDIAWIKI_API_ENDPOINT = 'https://en.wikipedia.org/w/index.php?oldid='#alternative for getting the html
MEDIAWIKI_API_ENDPOINT = 'https://en.wikipedia.org/api/rest_v1/page/html/'# see: https://en.wikipedia.org/api/rest_v1/?doc
STATIC_HTML_DUMP_ARTICLES_DIR = '/home/ddimitrov/wikipedia_html_dump/articles/'
STATIC_HTML_DUMP_ERRORS_DIR = '/home/ddimitrov/wikipedia_html_dump/error/'
# Limit the number of threads.
pool = threading.BoundedSemaphore(20)

def worker(u, article, iteration_number):
    headers = {'user-agent': EMAIL}
    # Request passed URL.
    r = requests.get(u, headers=headers, stream=True)
    directory = STATIC_HTML_DUMP_ARTICLES_DIR+str(iteration_number)
    try:
        os.mkdir(directory)
    except OSError, e:
        if e.errno == errno.EEXIST and os.path.isdir(directory):
            # File exists, and it's a directory,
            # another process beat us to creating this dir, that's OK.
            pass
        else:
            # Our target dir exists as a file, or different error,
            # reraise the error!
            raise
    error_directory = STATIC_HTML_DUMP_ERRORS_DIR+str(iteration_number)
    try:
        os.mkdir(error_directory)
    except OSError, e:
        if e.errno == errno.EEXIST and os.path.isdir(error_directory):
            # File exists, and it's a directory,
            # another process beat us to creating this dir, that's OK.
            pass
        else:
            # Our target dir exists as a file, or different error,
            # reraise the error!
            raise
    if not os.path.exists(error_directory):
        os.makedirs(error_directory)
    if r.status_code == 200:
        html_article_filename = STATIC_HTML_DUMP_ARTICLES_DIR+str(iteration_number)+'/article_'+str(article['id'])+'_' +\
                           str(article['rev_id'])+'.html'
        zip_article_filename = STATIC_HTML_DUMP_ARTICLES_DIR+str(iteration_number)+'/article_'+str(article['id'])+'_' +\
                                   str(article['rev_id'])+'.zip'
        handle_response(r, html_article_filename, zip_article_filename)
    else:
        html_article_filename = STATIC_HTML_DUMP_ERRORS_DIR+str(iteration_number)+'/article_'+str(article['id'])+'_' +\
                                   str(article['rev_id'])+'.html'
        zip_article_filename = STATIC_HTML_DUMP_ERRORS_DIR+str(iteration_number)+'/article_'+str(article['id'])+'_' +\
                                   str(article['rev_id'])+'.zip'
        handle_response(r, html_article_filename, zip_article_filename)

    # Release lock for other threads.
    pool.release()
    # Show the number of active threads.
    #print threading.active_count()

def req():
    # Get URLs from a text file, remove white space.
    db = MySQLDatabase(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
    db_worker_view = db.get_work_view()
    articles = db_worker_view.retrieve_all_articles()
    #articles = db_worker_view.retrieve_all_articles_questionmark()
    # measure time
    start = time.clock()
    start_time_iteration = start
    iteration_number = 483
    for i, article in enumerate(articles):
        # print some progress
        if i % 10000 == 0:
            #print time for the iteration
            seconds = time.clock() - start_time_iteration
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            print "Number of crawled articles: %d. Total time for last iteration of 10000 articles: %d:%02d:%02d" % (i, h, m, s)
            start_time_iteration = time.clock()
            iteration_number += 1

        # Thread pool.
        # Blocks other threads (more than the set limit).
        pool.acquire(blocking=True)
        # Create a new thread.
        # Pass each URL (i.e. u parameter) to the worker function.
        t = threading.Thread(target=worker, args=(MEDIAWIKI_API_ENDPOINT+urllib.quote(article['title'])+'/'+str(article['rev_id']), article, iteration_number))

        # Start the newly create thread.
        t.start()
    seconds = time.clock() - start
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    print "Total time: %d:%02d:%02d" % (h, m, s)


def handle_response(r, html_article_filename, zip_article_filename):
    with open(html_article_filename, 'wb') as outfile:
        for chunk in r.iter_content(1024):
            outfile.write(chunk)
        outfile.flush()
        outfile.close()
    zf = zipfile.ZipFile(zip_article_filename, mode='w', compression=zipfile.ZIP_DEFLATED)
    try:
        zf.write(html_article_filename, os.path.basename(html_article_filename))
        os.remove(html_article_filename)
    finally:
        zf.close()


req()
