__author__ = 'dimitrovdr'
from HTMLParser import HTMLParser


class WikipediaHTMLTableParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.fed = []
        self.fed_text = None
        self.table_counter = 0

    def reset(self):
        self.fed = []
        self.fed_text = None
        self.table_counter = 0
        HTMLParser.reset(self)

    def feed(self, data):
        self.reset()
        HTMLParser.feed(self, data)

    def handle_starttag(self, tag, attrs):
        if tag == 'table':
            attrs_dict = dict(attrs)
            if not self.table_counter:
                self.fed.append('[[[TABLE_BEGIN]]]\n')
                if 'class' in attrs_dict.keys():
                    self.fed.append('[[[TABLE_CLASS_BEGIN]]]')
                    self.fed.append(attrs_dict['class'])
                    self.fed.append('[[[TABLE_CLASS_END]]]\n')
            self.table_counter += 1

    def handle_endtag(self, tag):
        if tag == 'table':
            if self.table_counter:
                self.table_counter -= 1
                if not self.table_counter:
                    self.fed.append('[[[TABLE_END]]]\n')

    def get_data(self):
        if self.fed_text is not None:
            return self.fed_text
        else:
            self.fed_text = ''.join(self.fed)
            return self.fed_text


