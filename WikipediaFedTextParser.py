__author__ = 'dimitrovdr'
import re
from collections import Counter

class FedTextException(Exception):
    pass

class WikipediaFedTextParser():

    def __init__(self, fed_text):
        self.fed_text = self.__set_fed_text(fed_text)


    def reset(self):
        self.fed_text = None

    def get_text_only(self, data):
        if data is None:
            data = self.fed_text

        element_begin = '[[[TABLE_BEGIN]]]'
        element_end = '[[[TABLE_END]]]'

        index = 0
        text_only = []
        while index < len(data):
            index_begin = data.find(element_begin, index)
            if index_begin == -1:
                #append last part of the stirng and break
                text_only.append(data)
                break
            text_only.append(data[index:index_begin])
            index += len(element_begin)
            index_end = data.find(element_end, index)
            index_end += len(element_end)
            data = data[index_end:]
            index = 0
        return ''.join(text_only)


    def get_element(self, element_name, data):
        if data is None:
            data = self.fed_text
        element_begin = '[[['+element_name+'_BEGIN]]]'
        element_end = '[[['+element_name+'_END]]]'

        index = 0
        index_begin = []
        while index < len(data):
            index = data.find(element_begin, index)
            if index == -1:
                break
            index += len(element_begin)
            index_begin.append(index)

        index = 0
        index_end = []
        while index < len(data):
            index = data.find(element_end, index)
            if index == -1:
                break
            index_end.append(index)
            index += len(element_end)

        # begen number tags equels end number tags
        if len(index_end) != len(index_begin):
            raise FedTextException

        # no overlapping of tags
        overlapping = [(b, e) for b, e in zip(index_begin, index_end)]

        for i, e in enumerate(overlapping):
            if i > 0 and overlapping[i-1][1] > e[0]: #skip the first list element and test for overlapping
                raise FedTextException  # perhaps  better exception would be better i just don't know which in python

        #return snippets from text but also start and end postion of the snippets
        return [data[b:e] for b, e in overlapping], overlapping

    def get_links_position(self, data):
        if data is None:
            data = self.fed_text

        # replace all leading '[[[' and ending ']]]' so that we have just '[[link]]'
        data = data.replace("[[[", "").replace("]]]", "")
        # TODO check this regex
        tokens = data.split('\n')
        words = [t.strip() for t in tokens]
        words = [t for t in words if t]
        links = [link[2:-2] for link in words if link.startswith('[[')]
        return links

    def get_data_for_link(self, link):
        link_data = dict()
        # position in text
        link_data['target_position_in_text'] = self.position_in_text(link)

        section_number, section_name, position_in_section, position_in_section_in_text_only = self.section_data(link)
        # section number
        link_data['section_number'] = section_number

        # section name
        link_data['section_name'] = section_name

        # position in section
        link_data['target_position_in_section'] = position_in_section
        
        # position in section
        link_data['target_position_in_section_in_text_only'] = position_in_section_in_text_only

        table_number, table_class, table_style, position_in_table = self.table_data(link)

        # table number
        link_data['table_number'] = table_number

        # table class
        link_data['table_css_class'] = table_class

        # table style
        link_data['table_css_style'] = table_style

        # position in table
        link_data['target_position_in_table'] = position_in_table

        # position in text only
        link_data['target_position_in_text_only'] = self.position_in_text_only(None, link)

        para_number, position_in_para = self.paragraph_data(link)

        link_data['paragaph_number'] = para_number

        link_data['target_position_in_paragraph'] = position_in_para
        
        
        
        return link_data

    def __set_fed_text(self, fed_text):
        links = self.get_links_position(fed_text)
        counts = Counter(links)  # so we have: {'name':3, 'state':1, 'city':1, 'zip':2}
        for s, num in counts.items():
            if num > 1:  # ignore strings that only appear once
                for suffix in range(1, num + 1):  # suffix starts at 1 and increases by 1 each time
                    links[links.index(s)] = s + '-----##$$$##-----' + str(suffix)  # replace each appearance of s
        for s in links:  # replace each not unique link in fed_text with unique one
            if s.find('-----##$$$##-----')!=-1:
                search = s.split('-----##$$$##-----')[0]
                next_occ = fed_text.find('[['+search+']]')
                fed_text = fed_text[:next_occ] + '[[' + s + ']]' + fed_text[next_occ+len('[['+search+']]'):]
        return fed_text

    def position_in_text(self, link):
        links = self.get_links_position(None)
        return links.index(link) + 1

    def section_data(self, link):
        lead, lead_overlapping = self.get_element('LEAD', None)
        sections, overlapping = self.get_element('SECTION', None)
        lead += sections
        for i, section in enumerate(lead, 1):
            in_section = section.find('[['+link+']]')
            if in_section != -1:
                section_number = i
                section_name = self.get_element('SECTION_NAME', section)[0]
                if i == 1 and len(section_name) == 0:
                    section_name = 'Lead'
                else:
                    section_name = section_name[0]
                links = self.get_links_position(section)
                try:
                    position_in_section = links.index(link)+1
                except ValueError:
                    position_in_section = None
                # position in sections' text only
                position_in_section_in_text_only = self.position_in_text_only(section, link)
                return section_number, section_name, position_in_section, position_in_section_in_text_only
        return None, None, None

    def table_data(self, link):
        # get tables only
        tables_texts, tables_overlapping = self.get_element('TABLE', None)
        for i, table in enumerate(tables_texts, 1):
            in_table = table.find('[['+link+']]')
            if in_table != -1:
                table_number = i
                table_class = self.get_element('TABLE_CLASS', table)[0]
                table_style = self.get_element('TABLE_STYLE', table)[0]
                if len(table_class) == 0:
                    table_class = None
                else:
                    table_class = table_class[0]

                if len(table_style) == 0:
                    table_style = None
                else:
                    table_style = table_style[0]

                links = self.get_links_position(table)
                try:
                    position_in_table = links.index(link)+1
                except ValueError:
                    position_in_table = None
                return table_number, table_class, table_style, position_in_table
        return None, None, None, None

    def table_classes(self, data):
        # get tables only
        tables_texts, tables_overlapping = self.get_element('TABLE', None)
        return [self.get_element('TABLE_CLASS', table)[0][0] for table in tables_texts]



    def remove_link(self, link):
        next_occ = self.fed_text.find('[['+link+']]')
        self.fed_text = self.fed_text[:next_occ] + self.fed_text[next_occ+len('[['+link+']]'):]

    def position_in_text_only(self, data, link):
        if data is None:
            data = self.fed_text
        text_only = self.get_text_only(data)
        links = self.get_links_position(text_only)
        try:
            position = links.index(link)+1
        except ValueError:
            position = None
        return position


    def paragraph_data(self, link):
        # get paragraphs only
        para_texts, para_overlapping = self.get_element('PARA', None)
        for i, para in enumerate(para_texts, 1):
            in_para = para.find('[['+link+']]')
            if in_para != -1:
                para_number = i
                links = self.get_links_position(para)
                try:
                    position_in_para = links.index(link)+1
                except ValueError:
                    position_in_para = None
                return para_number, position_in_para
        return None, None
