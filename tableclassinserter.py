import copy_reg
import logging
import os
import types
import multiprocessing
from zipfile import ZipFile
import MySQLdb
from WikipediaFedTextParser import WikipediaFedTextParser
from WikipediaHTMLTableParser import WikipediaHTMLTableParser
from wsd.database import MySQLDatabase
from conf import *


def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)

copy_reg.pickle(types.MethodType, _pickle_method)




def build_table():
    """creates up the basic database structure
    """
    db = MySQLDatabase(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
    connection = db._create_connection()
    cursor = connection.cursor()

    cursor.execute('CREATE TABLE `table_css_class` ('
                      '`id` BIGINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,'
                      '`source_article_id` BIGINT UNSIGNED NOT NULL,'
                      ' css_class VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,'
                      'INDEX(`source_article_id`)'
                  ') ENGINE=InnoDB;')
    connection.close()


class Controller(object):
    def __init__(self):

        nProcess = 20
        self.manageWork(nProcess)

    def table_parser(self, file_name, root):

        db = MySQLDatabase(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
        db_build_view = db.get_build_view()

        cursor = db_build_view._cursor

        # setup logging
        LOGGING_FORMAT = '%(levelname)s:\t%(asctime)-15s %(message)s'
        LOGGING_PATH = 'tmp/tableclasses-dbinsert.log'
        logging.basicConfig(filename=LOGGING_PATH, level=logging.DEBUG, format=LOGGING_FORMAT, filemode='w')

        html_parser = WikipediaHTMLTableParser()
        zip_file_path = os.path.join(root, file_name)
        html = self.zip2html(zip_file_path)
        html_parser.feed(html.decode('utf-8'))
        source_article_id = file_name.split('_')[1]
        try:
            fed_parser = WikipediaFedTextParser(html_parser.get_data())
            table_classes = fed_parser.table_classes(None)
            table_classes = list(set(table_classes))
            for table_class in table_classes:
               self.insert_table_class(source_article_id, table_class, cursor)
        except KeyError:
            db_build_view._db_connection.rollback()
            logging.error('KeyError FedTextParser source article id: %s ' % source_article_id)
        db_build_view.commit()
        db_build_view.reset_cache()

    def zip2html(self, input_zip):
        input_zip = ZipFile(input_zip)
        files = {name: input_zip.read(name) for name in input_zip.namelist()}
        return files.popitem()[1]

    def insert_table_class(self, source_article_id, table_class, cursor):
        sql = "INSERT INTO table_css_class (source_article_id, css_class) VALUES (%s, %s);"
        try:
            cursor.execute(sql, (source_article_id,table_class))
            #logging.info('DB Insert Success for  target article id: "%s" ' % target_article_id)
        except MySQLdb.Error, e:
            logging.error('DB Insert Error source article id: "%s" ' % source_article_id)
        return source_article_id

    def manageWork(self, nProcess):
        #STATIC_HTML_DUMP_ARTICLES_DIR = '/home/ddimitrov/wikipedia_html_dump/articles/'
        pool = multiprocessing.Pool(processes=nProcess)
        for dirname, dirnames, filenames in os.walk(STATIC_HTML_DUMP_ARTICLES_DIR):
            for subdirname in dirnames:
                for root, dirs, files in os.walk(os.path.join(STATIC_HTML_DUMP_ARTICLES_DIR, subdirname)):
                    for file_name in files:
                        if file_name.endswith(".zip"):
                            pool.apply_async(self.table_parser, args=(file_name, root, ))
        pool.close()
        pool.join()



if __name__ == '__main__':
    build_table()
    Controller()