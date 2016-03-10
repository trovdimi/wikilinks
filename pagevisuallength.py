from collections import Counter
import copy_reg
import logging
import os
import types
import multiprocessing
from zipfile import ZipFile
import MySQLdb
from PyQt4.QtCore import QUrl, QString
from PyQt4.QtGui import QApplication
import sys
import requests
from WikiBrowser import WikiBrowser
from wsd.database import MySQLDatabase
from collections import deque
from bs4 import BeautifulSoup as Soup
import time
from conf import *

def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)

copy_reg.pickle(types.MethodType, _pickle_method)


def build_page_length_table():
    """creates up the basic database structure
    """
    db = MySQLDatabase(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
    connection = db._create_connection()
    cursor = connection.cursor()

    # build page_length table
    cursor.execute('CREATE TABLE `page_length` ('
                      '`id` BIGINT UNSIGNED NOT NULL PRIMARY KEY,'
                      ' page_length_1920_1080 INT UNSIGNED DEFAULT NULL'
                  ') ENGINE=InnoDB;')
    connection.close()




class Controler(object):
    def __init__(self, path):
        print path
        os.environ["DISPLAY"]=":1"
        self.app = QApplication(sys.argv)
        self.path = path
        nProcess = 15
        #self.app.exec_()
        #self.manageWork(nProcess)

    def parse_article(self, file_name, root):


        # setup logging
        LOGGING_FORMAT = '%(levelname)s:\t%(asctime)-15s %(message)s'
        LOGGING_PATH = 'tmp/pagelength-dbinsert-'+self.path+'.log'
        logging.basicConfig(filename=LOGGING_PATH, level=logging.ERROR, format=LOGGING_FORMAT, filemode='w')

        zip_file_path = os.path.join(root, file_name)
        html = self.zip2html(zip_file_path)
        source_article_id = file_name.split('_')[1]
        #if source_article_id == '3240901':
        try:
            html = self.insert_last_tag(html, source_article_id)
            positions = self.get_screen_positions_qt(html.decode('utf-8'))
        except Exception, e:
            print "FAIL"
            print zip_file_path
            print e
        #try:
        #positions = self.get_screen_positions_qt(html.decode('utf-8'))
            #if positions['1366_768'] is not None and positions['1920_1080'] is not None:
            #            self.insert_pagelength(source_article_id,
            #                                   positions['1366_768'],
            #                                   positions['1920_1080'],
            #                              cursor)

            #else:
            #             self.insert_pagelength(source_article_id,
            #                             None,
            #                             None,
            #                             cursor)
        #except Exception as e:
        #    logging.error(e)
        #    db_build_view._db_connection.rollback()
        #    logging.error('Exception source article id: %s ' % source_article_id)
        #db_build_view.commit()
        #db_build_view.reset_cache()


    def zip2html(self, input_zip):
        input_zip = ZipFile(input_zip)
        files = {name: input_zip.read(name) for name in input_zip.namelist()}
        return files.popitem()[1]

    def insert_pagelength(self, source_article_id, screen_positions_1366_768,
                    screen_positions_1920_1080, cursor):

            data={}
            data['source_article_id'] = source_article_id
            if screen_positions_1366_768 is not None and screen_positions_1920_1080 is not None:
                data['page_length_1366_768'] = screen_positions_1366_768
                data['page_length_1920_1080'] = screen_positions_1920_1080
            else:
                data['page_length_1366_768'] = None
                data['page_length_1920_1080'] = None
            #print data
            sql = "INSERT INTO page_length (id,  page_length_1366_768, page_length_1920_1080) VALUES" \
                   "(%(source_article_id)s, %(page_length_1366_768)s, %(page_length_1920_1080)s);"
            try:
                cursor.execute(sql, data)
            except MySQLdb.Error, e:
                logging.error('DB Insert Error  page length for id: "%s" ' % source_article_id)



    def manageWork(self):
        print "manage"
        #pool = multiprocessing.Pool(processes=nProcess)
        for root, dirs, files in os.walk(STATIC_HTML_DUMP_ARTICLES_DIR + self.path):
            #print "o"
            for i, file_name in enumerate(files):
                if file_name.endswith(".zip"):
                    self.parse_article(file_name,root)
                    #pool.apply_async(self.parse_article, args=(file_name, root, ))
        #pool.close()
        #pool.join()


    def get_screen_positions_qt(self, html):

        #app = QApplication(sys.argv)
        positions = {}
        positions['1920_1080'] = self.render_for_resolution_qt((1920, 1080), html)
        positions['1366_768'] = self.render_for_resolution_qt((1366, 768), html)
        print self.path, positions
        return positions

    def render_for_resolution_qt(self, resolution, html):
        browser = WikiBrowser(html, resolution)

        while not browser.finished:
            self.app.processEvents()

        #print browser.page_length
        return browser.page_length

        self.app.exec_()






    def insert_last_tag(self, html, source_article_id):
        # we need this in order to plot the heatmap
        soup = Soup(html, 'html.parser')
        head = soup.find('base')
        print soup.find("title")
        if head is not None:
	   head.decompose()
        #head['href']= "file:///home/ddimitrov/wikiwsd/data/"
        
	css = soup.find("link", {"rel": "stylesheet"})
        if css is not None:
	   css['href']= 'https:'+css['href']
           headers = {'user-agent': EMAIL}
           r = requests.get(css['href'], headers=headers, stream=True)
           css['href']= ""
           if r.status_code == 200:
              style = soup.new_tag('style')
              style.string=r.text
              css.insert_after(style)
           else:
              logging.error('Cannot load css  for id: "%s" ' % source_article_id)
          
           css.decompose()
	  
        #css['href'] = "file:///home/ddimitrov/wikiwsd/wikipedia_css.css"
        #css['type'] = "text/css"
        last_element_on_page_meta = soup.new_tag('meta')
        last_element_on_page_meta['http-equiv'] = "content-type"
        last_element_on_page_meta['content'] = "text/html; charset=utf-8"
        
	body = soup.find('body')
        #if body is not None:
	last_element_on_page = soup.new_tag('div')
        last_element_on_page['class']="pyqt_is_shit"
        body.append(last_element_on_page)
        return soup.prettify(encoding='utf-8')




if __name__ == '__main__':
        #build_page_length_table()
        #print "wooo"
        print sys.argv
        c = Controler(sys.argv[1])
        c.manageWork()
        #Controler('77')
        #return 1
