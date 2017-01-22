from collections import Counter
import copy_reg
import logging
import os
import types
import multiprocessing
from multiprocessing.pool import ThreadPool
import urllib
import warnings
from zipfile import ZipFile
import zipfile
import MySQLdb
from PyQt4.QtCore import QCoreApplication
from PyQt4.QtGui import QApplication
import sys
import time
import requests
from xvfbwrapper import Xvfb
from WikiBrowser import WikiBrowser
from WikipediaFedTextParser import WikipediaFedTextParser, FedTextException
from WikipediaHTMLParser import WikipediaHTMLParser
from wsd.database import MySQLDatabase
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup as Soup
import codecs as cd
from pyvirtualdisplay import Display
from conf import *
import pickle


def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)

copy_reg.pickle(types.MethodType, _pickle_method)


class Controller(object):
    def __init__(self, path):
        #os.environ["DISPLAY"]=":1"
        print path
        os.environ["DISPLAY"]=":1"
        db = MySQLDatabase(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
        self.db_build_view = db.get_build_view()
        self.cursor = self.db_build_view._cursor

        self.app = QApplication(sys.argv)
        self.path = path

    def parse_article(self, file_name, root):

        html_parser = WikipediaHTMLParser()
        zip_file_path = os.path.join(root, file_name)
        html = self.zip2html(zip_file_path)
        html_parser.feed(html.decode('utf-8'))
        source_article_id = file_name.split('_')[1]
        positions = None
        page_length = None
        #if source_article_id in['33613763','39980984', '4232982','4243416', '4122301', '33610181','120539', '120538', '120543']:
        #if source_article_id in['3550838']:
        try:
            html = self.modify_html(html, source_article_id)
            #html = html.decode('utf-8')
            page_length, positions = self.get_screen_positions_qt(html.decode('utf-8'))
            #print positions
        except Exception, e:
            print "FAIL: HTML/POSITION"
            print zip_file_path
            print e

        # try:
        #     self.insert_pagelength(source_article_id, page_length, zip_file_path)
        # except Exception as e:
        #    self.db_build_view._db_connection.rollback()
        #    self.db_build_view.commit()
        #    print "FAIL: INSERT PAGELENGTH"
        #    print zip_file_path
        #    print e
        #
        # try:
        #     fed_parser = WikipediaFedTextParser(html_parser.get_data())
        #     links = fed_parser.get_links_position(None)
        #
        #     #resolve links remove not found articles and set the fed_text
        #     for link in links:
        #         if self.db_build_view._resolve_title(link.split('-----##$$$##-----')[0].replace('_', ' ')) is None:
        #             fed_parser.remove_link(link)
        #     #get links again, no unresolve links in fed_text now
        #     links = fed_parser.get_links_position(None)
        #
        #     if positions is not None:
        #         for link in links:
        #             try:
        #
        #                 position = positions[link]
        #
        #                 self.insert_link(source_article_id, link, fed_parser.get_data_for_link(link),
        #                                  position, zip_file_path)
        #             except KeyError:
        #                 self.insert_link(source_article_id, link, fed_parser.get_data_for_link(link),
        #                                                          None, zip_file_path)
        #                 print('FAIL: KeyError Link Position dict for source article id: %s ' % source_article_id)
        #                 print zip_file_path
        #
        #     else:
        #         for link in links:
        #             try:
        #                  self.insert_link(source_article_id, link, fed_parser.get_data_for_link(link),
        #                                  None, zip_file_path)
        #             except KeyError:
        #                 print('FAIL: KeyError Link Position dict for source article id: %s ' % source_article_id)
        #                 print zip_file_path
        # except FedTextException:
        #     self.db_build_view._db_connection.rollback()
        #     print('FAIL: KeyError FedTextParser source article id: %s ' % source_article_id)
        #     print zip_file_path
        # except Exception as e:
        #     self.db_build_view._db_connection.rollback()
        #     print('FAIL: Exception source article id: %s ' % source_article_id)
        #     print zip_file_path
        #     print e
        # self.db_build_view.commit()
        # self.db_build_view.reset_cache()


    def zip2html(self, input_zip):
        input_zip = ZipFile(input_zip)
        files = {name: input_zip.read(name) for name in input_zip.namelist()}
        return files.popitem()[1]

    def insert_pagelength(self, source_article_id, screen_positions_1920_1080, zip_file_path):

               data={}
               data['source_article_id'] = source_article_id
               if screen_positions_1920_1080 is not None:
                   data['page_length_1920_1080'] = screen_positions_1920_1080
               else:
                   data['page_length_1920_1080'] = None
               #print data
               sql = "INSERT INTO redirects_candidates_page_length (id, page_length_1920_1080) VALUES" \
                      "(%(source_article_id)s, %(page_length_1920_1080)s);"
               try:
                   self.cursor.execute(sql, data)
               except (MySQLdb.Error, MySQLdb.Warning), e:
                   print ('FAIL: Data caused warning or error "%s" for source_article_id: "%s"', data,  source_article_id)
                   print 'FAIL: EXCEPTION:', e
                   print zip_file_path


    def insert_link(self, source_article_id, target_article_name, data, position,  zip_file_path):

        target_article_id = self.db_build_view._resolve_title(target_article_name.split('-----##$$$##-----')[0].replace('_', ' '))
        data['target_article_name'] = target_article_name.split('-----##$$$##-----')[0].replace('_', ' ')
        data['source_article_id'] = source_article_id
        data['target_article_id'] = target_article_id
        if position is not None:
            data['target_x_coord_1920_1080'] = position[0]
            data['target_y_coord_1920_1080'] = position[1]
            if data['target_y_coord_1920_1080'] < 0:
                data['target_y_coord_1920_1080'] = 0
        else:
            data['target_x_coord_1920_1080'] = None
            data['target_y_coord_1920_1080'] = None
        #print data
        sql = "INSERT INTO redirects_candidates (source_article_id, target_article_id, target_article_name," \
               "target_position_in_text, target_position_in_text_only, target_position_in_section, " \
               "target_position_in_section_in_text_only, section_name," \
               " section_number, target_position_in_table, table_number, table_css_class, table_css_style," \
               " target_x_coord_1920_1080, target_y_coord_1920_1080) VALUES" \
               "(%(source_article_id)s, %(target_article_id)s, %(target_article_name)s, %(target_position_in_text)s," \
               "%(target_position_in_text_only)s, %(target_position_in_section)s,  %(target_position_in_section_in_text_only)s, " \
               "%(section_name)s, %(section_number)s, %(target_position_in_table)s, %(table_number)s, " \
               "%(table_css_class)s, %(table_css_style)s," \
               "%(target_x_coord_1920_1080)s, %(target_y_coord_1920_1080)s);"
        try:
            self.cursor.execute(sql, data)
            #logging.info('DB Insert Success for  target article id: "%s" ' % target_article_id)
        except (MySQLdb.Error, MySQLdb.Warning), e:
            #print sql
            print ('FAIL: Data caused warning or error "%s" for target_article_id: "%s" in for source_article_id: "%s"', data, target_article_id, source_article_id)
            print 'FAIL: EXCEPTION:', e
            print zip_file_path
            #print('DB Insert Error  target article id: "%s" ' % target_article_id)
        return target_article_id

    def manageWork(self):
        #file = open("/home/ddimitrov/20160305_en_wikilinks/tmp/missing_article_ids.p",'r')
        file = open(SSD_HOME+"pickle/redirects_ids.obj",'r')
        object_file = pickle.load(file)
        #print object_file
        #print type(object_file)
        for root, dirs, files in os.walk(STATIC_HTML_DUMP_ARTICLES_DIR+self.path):
            for i, file_name in enumerate(files):
                if file_name.endswith(".zip"):
                    parts = file_name.split('_')
                    if long(parts[1]) in object_file:

                        try:
                            self.parse_article(file_name,root)
                        except  Exception as e:
                            print("FILENAME_FAIL:"+file_name)
                            print(type(e))    # the exception instance
                            print(e)
                            print (e.message)



    def get_screen_positions_qt(self, html):
        return self.render_for_resolution_qt((1920, 1080), html)

    def render_for_resolution_qt(self, resolution, html):
        browser = WikiBrowser(html, resolution)
        while not browser.finished:
            self.app.processEvents()

        #print browser.page_length
        return browser.page_length, browser.positions




    def insert_header(self, html_file_name, html):
        # we need to do this since the crawled files dont have excplicitly stated content type but the
        # phantomjs depends on it to render the file properly
        soup = Soup(html, 'html.parser')
        title = soup.find('title')
        meta = soup.new_tag('meta')
        meta['content'] = "text/html; charset=UTF-8"
        meta['http-equiv'] = "Content-Type"
        title.insert_after(meta)

        with cd.open(html_file_name, mode='w', encoding='utf-8') as f:
            f.write(soup.prettify())
        f.close()


    def modify_html(self, html, source_article_id):
        # we need this in order to plot the heatmap
        soup = Soup(html, 'html.parser')
        head = soup.find('base')
        print soup.find("title")
        if head is not None:
            head.decompose()


        css = soup.find("link", {"rel": "stylesheet"})
        if css is not None:
            css['href'] = 'https:' + css['href']
            headers = {'user-agent': EMAIL}
            r = requests.get(css['href'], headers=headers, stream=True)
            css['href'] = ""
            if r.status_code == 200:
                style = soup.new_tag('style')
                style.string = r.text
                css.insert_after(style)
            else:
                print('FAIL: Cannot load css  for id: "%s" ' % source_article_id)

            css.decompose()

        last_element_on_page_meta = soup.new_tag('meta')
        last_element_on_page_meta['http-equiv'] = "content-type"
        last_element_on_page_meta['content'] = "text/html; charset=utf-8"

        body = soup.find('body')
        #if body is not None:
        last_element_on_page = soup.new_tag('div')
        last_element_on_page['class'] = "pyqt_is_shit"
        body.append(last_element_on_page)
        return soup.prettify(encoding='utf-8')



if __name__ == '__main__':
    print sys.argv
    warnings.filterwarnings('error', category=MySQLdb.Warning)
    #c = Controller(sys.argv[1])
    c = Controller('1')
    c.manageWork()



