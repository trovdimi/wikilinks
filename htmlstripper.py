import copy_reg
import logging
import os
import types
import multiprocessing
import zipfile
import codecs
from MLStripper import MLStripper
from conf import *



def _pickle_method(m):
    if m.im_self is None:
        return getattr, (m.im_class, m.im_func.func_name)
    else:
        return getattr, (m.im_self, m.im_func.func_name)

copy_reg.pickle(types.MethodType, _pickle_method)

# setup logging
LOGGING_FORMAT = '%(levelname)s:\t%(asctime)-15s %(message)s'
LOGGING_PATH = 'tmp/stripper.log'
logging.basicConfig(filename=LOGGING_PATH, level=logging.DEBUG, format=LOGGING_FORMAT, filemode='w')


class Controller(object):
    def __init__(self):
        nProcess = 20
        self.manageWork(nProcess)

    def html_stripper(self, file_name, root, subdirname):
        zip_file_path = os.path.join(root, file_name)
        html = self.zip2html(zip_file_path)
        plaintext = self.strip_tags(html.decode('utf-8'))
        self.plaintext2zip(file_name, subdirname, plaintext)


    def zip2html(self, input_zip):
        input_zip = zipfile.ZipFile(input_zip)
        files = {name: input_zip.read(name) for name in input_zip.namelist()}
        return files.popitem()[1]

    def strip_tags(self, html):
        s = MLStripper()
        s.feed(html)
        return s.get_data()

    def plaintext2zip(self, file_name, subdirname, plaintext):

        file_name=file_name.split('.')[0]
        plaintext_file_name = STATIC_PLAINTEXT_ARTICLES_DIR+subdirname+'/'+file_name+'.txt'
        zip_file_name = STATIC_PLAINTEXT_ARTICLES_DIR+subdirname+'/'+file_name+'.zip'

        if not os.path.exists(STATIC_PLAINTEXT_ARTICLES_DIR+subdirname):
            os.makedirs(STATIC_PLAINTEXT_ARTICLES_DIR+subdirname)


        with codecs.open(plaintext_file_name, 'w', encoding='utf8') as outfile:
            outfile.write(plaintext)
            outfile.flush()
            outfile.close()

        zf = zipfile.ZipFile(zip_file_name, mode='w', compression=zipfile.ZIP_DEFLATED)
        try:
            zf.write(plaintext_file_name, os.path.basename(plaintext_file_name))
            os.remove(plaintext_file_name)
        except Exception, e:
            print e
            logging.error('zip error %s ' % plaintext_file_name)
        finally:
            zf.close()




    def manageWork(self, nProcess):
        pool = multiprocessing.Pool(processes=nProcess)
        for dirname, dirnames, filenames in os.walk(STATIC_HTML_DUMP_ARTICLES_DIR):
            for subdirname in dirnames:
                for root, dirs, files in os.walk(os.path.join(STATIC_HTML_DUMP_ARTICLES_DIR, subdirname)):
                    for file_name in files:
                        if file_name.endswith(".zip"):
                            pool.apply_async(self.html_stripper, args=(file_name, root, subdirname,))
        pool.close()
        pool.join()



if __name__ == '__main__':
    Controller()