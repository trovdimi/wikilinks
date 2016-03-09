import os
import subprocess
from linkpostioninserter import Controler
from wsd.database import MySQLDatabase
import sys
import time
from dbsettings import *
__author__ = 'dimitrovdr'

def build_links_position_table():
    """creates up the basic database structure
    """
    db = MySQLDatabase(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
    connection = db._create_connection()
    cursor = connection.cursor()

    cursor.execute('CREATE TABLE `links` ('
                      '`id` BIGINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,'
                      '`source_article_id` BIGINT UNSIGNED NOT NULL,'
                      '`target_article_id` BIGINT UNSIGNED NOT NULL,'
                      ' target_position_in_text INT UNSIGNED NOT NULL,'
                      ' target_position_in_text_only INT UNSIGNED,'
                      ' target_position_in_section INT UNSIGNED,'
                      ' target_position_in_section_in_text_only INT UNSIGNED,'
                      ' section_name VARCHAR(1000) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,'
                      ' section_number INT UNSIGNED,'
                      ' target_position_in_table INT UNSIGNED,'
                      ' table_number INT UNSIGNED,'
                      ' table_css_class VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_bin,'
                      ' table_css_style VARCHAR(255) CHARACTER SET utf8 COLLATE utf8_bin,'
                      ' target_x_coord_1920_1080 INT UNSIGNED DEFAULT NULL,'
                      ' target_y_coord_1920_1080 INT UNSIGNED DEFAULT NULL ,'
                      ' target_position_in_paragraphs INT UNSIGNED,'
                      ' target_position_in_paragraph INT UNSIGNED,'
                      ' paragraph_number INT UNSIGNED,'
                      'INDEX(`target_article_id`),'
                      'INDEX(`source_article_id`)'
                  ') ENGINE=InnoDB;')
    connection.close()


def build_page_length_table():
    """creates up the basic database structure
    """
    db = MySQLDatabase(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
    connection = db._create_connection()
    cursor = connection.cursor()

    cursor.execute('CREATE TABLE `page_length` ('
                      '`id` BIGINT UNSIGNED NOT NULL PRIMARY KEY,'
                      ' page_length_1920_1080 INT UNSIGNED DEFAULT NULL'
                  ') ENGINE=InnoDB;')
    connection.close()


def worker(dir):
    c = Controler(dir)
    c.manageWork(1)

#build_page_length_table()
print 'start'
#p = subprocess.Popen(['python linkpostioninserter.py 1'])
#p.wait()

#p = multiprocessing.Pool(1)
build_links_position_table()
build_page_length_table()
zips = []

#STATIC_HTML_DUMP_ARTICLES_DIR = '/home/ddimitrov/wikipedia_html_dump/articles/'
for dirname, dirnames, filenames in os.walk(STATIC_HTML_DUMP_ARTICLES_DIR):
    #print "a"
    for i, subdirname in enumerate(dirnames):
        zips.append(subdirname)
        #break
    #break

print "zips", len(zips)

max_task = 20
processes = []

while True:
    while zips and len(processes) < max_task:
        task = zips.pop()
        fout = open("stdout/stdout_%s.txt" % task,'w')
        #processes.append(subprocess.Popen(['python', '/home/ddimitrov/wikiwsd/linkpostioninserter.py', task],  stdout=fout))
        processes.append(subprocess.Popen(['python', 'linkpostioninserter.py', task],  stdout=fout))

    for p in processes:
        if p.poll() is not None:
            if p.returncode == 0:
                processes.remove(p)
            else:
                sys.exit(1)

    if not processes and not zips:
        break
    else:
        time.sleep(0.05)

        #print "b"
        #p.apply_async(worker,(subdirname,))i
#        print subdirname
#p = subprocess.Popen('python /home/ddimitrov/wikiwsd/pagevisuallength.py',#+subdirname,
                        #stdin=subprocess.PIPE,
 #                       shell=True,
 #                       stdout=subprocess.PIPE,
 #                       bufsize=1
 #                       )
#for line in iter(p.stdout.readline, b''):
#    print line,
#p.stdout.close()
#p.wait()

#while proc.poll() is Nonie:
#    l = proc.stdout.readline() # This blocks until it receives a newline.
#    print l

#process.communicate()
#        break
#    break
#p.close()
#p.join()



print 'done'
