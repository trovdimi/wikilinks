from PyQt4 import QtGui
import codecs
from collections import Counter
import os
from PyQt4.QtCore import QSize, QUrl, QString, pyqtSignal, pyqtSlot
from PyQt4.QtGui import QApplication, QMainWindow, QWidget, QImage, QPainter
from PyQt4.QtWebKit import QWebView, QWebPage, QWebSettings, QWebFrame
import sys
import time
from xvfbwrapper import Xvfb
import random


class WikiBrowser(QWebView):

    ''' Represents a punching bag; when you punch it, it
            emits a signal that indicates that it was punched. '''
    punched = pyqtSignal(int)

    def __init__(self, html, resolution):

        QWebView.__init__(self)
        self.resolution = resolution
        self.finished = False
        self.out = "web2png.%i.png"%int(random.randint(0,1000))

        #self.web_view = QWebView()
        #self.css_file = QString('/home/ddimitrov/wikiwsd/data/wikipedia_css.css')
        #path = os.getcwd()

        #self.settings().setAttribute(QWebSettings.LocalContentCanAccessRemoteUrls, True)
        #self.settings().setAttribute(QWebSettings.LocalContentCanAccessFileUrls, True)
        #self.web_view.settings().setUserStyleSheetUrl(QUrl.fromLocalFile("wikipedia_css.css"))

        #self.web_view.settings().setUserStyleSheetUrl(QUrl.fromLocalFile(QString('file:///home/ddimitrov/wikiwsd/wikipedia_css.css')))
        #print self.web_view.settings().userStyleSheetUrl()
        #self.web_view.settings().setAttribute(QWebSettings.AutoLoadImages, False)
        #self.web_view.settings().setAttribute(QWebSettings.JavascriptEnabled, False)
        #self.setCentralWidget(self.web_view)
        
        #self.resize(resolution[0], resolution[1])
        
        self.loadFinished.connect(self._load_finished)
        #self.loadProgress.connect(self._loadProgress)
        
        self.setHtml(html)
       
        #self.page_length = None
        #self.positions = None
        #self.out = "web2png.%i.png"%int(time.time())


    def _loadProgress(self, result):
            print result

    def set_resolution(self,resolution):
        self.resolution=resolution

    def _load_finished(self):
        #print "finished"
        frame = self.page().mainFrame()
        size = QSize(self.resolution[0], self.resolution[1])
        self.page().setPreferredContentsSize(size)
        self.resize(frame.contentsSize())
        self.page().setViewportSize(frame.contentsSize())
        html = frame.documentElement()

        #two modes for these lines of code: page lenght and links position mode: page length activeted
        keys = []
        values = []
        for link in html.findAll('a'):
            href = unicode(link.attribute('href'))
            if href.startswith('./'):
                key = href.split('./')[-1].split('#')[0]
                keys.append(key)
                value = link.geometry().topLeft().x(), link.geometry().topLeft().y()
                values.append(value)

        counts = Counter(keys)  # so we have: {'name':3, 'state':1, 'city':1, 'zip':2}
        for s, num in counts.items():
            if num > 1:  # ignore strings that only appear once
                for suffix in range(1, num + 1):  # suffix starts at 1 and increases by 1 each time
                    keys[keys.index(s)] = s + '-----##$$$##-----' + str(suffix)
        self.positions = {k: v for k, v in zip(keys, values)}
        img = QImage(frame.contentsSize(), QImage.Format_ARGB32)
        paint = QPainter(img)
        print("rendering...")
        frame.render(paint)
        paint.end()
        img.save(self.out+"_"+str(self.resolution[0])+".png")
        print("... done")
        print("result: %s"%self.out)
        #print  html.findFirst("div[class=pyqt_is_shit]").geometry().topLeft().y()
        self.page_length = html.findFirst("div[class=pyqt_is_shit]").geometry().topLeft().y()
        print self.page_length
        #self.punched.emit(self.page_length)
        #self.close()
        #print "done"
        self.finished = True
        #self.quit()

    def get_positions(self):
        return self.positions

    def get_page_length(self):
        return self.page_length







if __name__ == '__main__':
    #vdisplay = Xvfb()
    #vdisplay.start()
    os.environ["DISPLAY"]=":1"
    app = QApplication(sys.argv)
    #browser = WikiBrowser((1366,768))
    #r = QUrl("./data/Ben_Eastman.html")
    #read_data=''
    with codecs.open('./data/Anarchism.htm', mode='r', encoding='utf-8') as f:
        read_data = f.read()
    #browser.web_view.setHtml(read_data, QUrl(QString('file:///home/ddimitrov/wikiwsd/data/')))
    #browser.web_view.setHtml(read_data)
    browser = WikiBrowser(read_data,(1920, 1080))
    while not browser.finished:
        app.processEvents()

        #print browser.page_length
    print browser.page_length

    #vdisplay.stop()

