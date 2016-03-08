__author__ = 'dimitrovdr'


from HTMLParser import HTMLParser

class WikipediaHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.fed = []
        self.fed_in_section = []
        self.fed_text = None
        self.section_found = False
        self.section_name = False
        self.table_counter = 0
        self.lead_found = False
        self.tracking_link = False
        self.tracking_see_also = False
        self.navbox_counter = 0
        self.in_section = False
        self.paragraph_found = False
        self.paragraph_counter = 0

    def reset(self):
        self.fed = []
        self.fed_in_section = []
        self.fed_text = None
        self.section_found = False
        self.section_name = False
        self.table_counter = 0
        self.lead_found = False
        self.tracking_link = False
        self.tracking_see_also = False
        self.navbox_counter = 0
        self.in_section = False
        self.paragraph_found = False
        self.paragraph_counter = 0
        HTMLParser.reset(self)

    def feed(self, data):
        self.reset()
        HTMLParser.feed(self, data)

    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            try:
                href = next(a[1] for a in attrs if a[0] == 'href')
                if href.startswith('./'):
                    if not self.in_section:
                        self.fed.append(' [[' + href.split('./')[-1].split('#')[0])
                    else:
                        self.fed_in_section.append(' [[' + href.split('./')[-1].split('#')[0])
                    self.tracking_link = True
            except StopIteration:
                pass

        elif tag == 'h2':
            self.in_section = True
            if not self.lead_found:
                self.fed.append('[[[LEAD_END]]]\n')       #new lines  are important for the further parsing with the FedTextParser
                self.fed.append('[[[SECTION_BEGIN]]]\n')
                self.lead_found = True
            else:
                self.fed.append('[[[SECTION_END]]]\n')
                self.fed.append('[[[SECTION_BEGIN]]]\n')
            self.section_found = True
            self.section_name = True

        elif tag == 'table':
            attrs_dict = dict(attrs)
            if any(['box' in v for v in attrs_dict.values()]) \
                    or any(['event' in v for v in attrs_dict.values()])\
                    or any(['metadata' in v for v in attrs_dict.values()]) \
                    or any(['toc' in v for v in attrs_dict.values()]) \
                    or any(['tracklist' in v for v in attrs_dict.values()])\
                    or any(['table' in v for v in attrs_dict.values()])\
                    or any(['person' in v for v in attrs_dict.values()])\
                    or any(['multicol' in v for v in attrs_dict.values()])\
                    or any(['cquote' in v for v in attrs_dict.values()]):
                if not self.table_counter:
                    self.fed.append('[[[TABLE_BEGIN]]]\n')
                    if 'style' in attrs_dict.keys():
                        style_dict = dict(item.strip().split(":") for item in attrs_dict['style'].split(";") if len(item.strip()) > 0 and len(item.strip().split(":"))==2)
                        if 'float' in style_dict.keys():
                            self.fed.append('[[[TABLE_STYLE_BEGIN]]]')
                            self.fed.append(style_dict['float'])
                            self.fed.append('[[[TABLE_STYLE_END]]]\n')
                    if 'class' in attrs_dict.keys():
                        self.fed.append('[[[TABLE_CLASS_BEGIN]]]')
                        self.fed.append(attrs_dict['class'])
                        self.fed.append('[[[TABLE_CLASS_END]]]\n')
                self.table_counter += 1
        elif tag == 'p':
            self.paragraph_found = True
            if not self.paragraph_counter:
                self.fed.append('[[[PARA_BEGIN]]]\n')
            self.paragraph_counter += 1




    def handle_endtag(self, tag):
        if tag == 'a' and self.tracking_link:
            if not self.in_section:
                self.fed.append(']]\n')
            else:
                self.fed_in_section.append(']]\n')
            self.tracking_link = False
        elif tag == 'table':
            if self.table_counter:
                self.table_counter -= 1
                if not self.table_counter:
                    self.fed.append('[[[TABLE_END]]]\n')
        elif tag == 'h2':
            self.in_section = False
            self.fed.extend(self.fed_in_section)
            self.fed_in_section = []
        elif tag == 'p':
            if self.paragraph_counter:
                self.paragraph_counter -= 1
                if not self.paragraph_counter:
                    self.fed.append('[[[PARA_END]]]\n')

    def handle_data(self, d):
        if self.section_name:
            self.fed.append('[[[SECTION_NAME_BEGIN]]]'+d+'[[[SECTION_NAME_END]]]\n')
            self.section_name = False

    def get_data(self):
        if self.fed_text is not None:
            return self.fed_text
        else:
            self.fed = ['[[[LEAD_BEGIN]]]\n'] + self.fed
            if self.section_found:
                self.fed.append('[[[SECTION_END]]]\n')
            else:
                self.fed.append('[[[LEAD_END]]]\n')
            self.fed_text = ''.join(self.fed)
            return self.fed_text

