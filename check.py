# -*- coding: utf-8 -*-

from __future__ import print_function

import atexit
import collections
import cPickle as pickle
import gzip
import json
import io
import numpy as np
import os
import pandas as pd
import pdb
import re
import urllib
from wsd.database import MySQLDatabase
from graph_tool.all import *
from conf import *
from wsd.database import MySQLDatabase
from graph_tool.all import *
from conf import *



import decorators

# set a few options
pd.options.mode.chained_assignment = None
pd.set_option('display.width', 400)


class DataHandler(object):
    def __init__(self):
        pass

    @staticmethod
    def unescape_mysql(title):
        # via dev.mysql.com/doc/refman/5.0/en/string-literals.html
        return title.replace("\\'", "'")\
                    .replace('\\"', '"')\
                    .replace('\\_', '_')\
                    .replace('\\%', '%')\
                    .replace('\\\\', '\\')

    @decorators.Cached
    def get_title2id(self, dump_date):
        print('get_title2id...')
        title2id = {}
        regex = re.compile(r"\((\d+),0,'(.+?)','")
        fname = '/home/ddimitrov/data/enwiki20150304_plus_clickstream/enwiki-' + dump_date + '-page.sql.gz'
        fname = '/home/ddimitrov/data/enwiki20150304_plus_clickstream/enwiki-' + dump_date + '-page.sql'
        #with gzip.GzipFile(fname, 'rb') as infile:
        with open(fname) as f:
            content = f.readlines()
            for line in content:
                line = line.decode('utf-8')
                if not line.startswith('INSERT'):
                    continue
                for pid, title in regex.findall(line):
                    title2id[DataHandler.unescape_mysql(title)] = int(pid)

        return title2id

    def write_pickle(self, fpath, obj):
        with open(fpath, 'wb') as outfile:
            pickle.dump(obj, outfile, -1)

    @decorators.Cached
    def get_rpid2pid(self, dump_date):
        print('get_rpid2pid...')
        title2id = self.get_title2id(dump_date)
        rpid2pid = {}
        regex = re.compile(r"\((\d+),0,'(.+?)','")
        fname = '/home/ddimitrov/data/enwiki20150304_plus_clickstream/enwiki-' + dump_date + '-redirect.sql.gz'
        with gzip.GzipFile(fname, 'rb') as infile:
            for line in infile:
                line = line.decode('utf-8')
                if not line.startswith('INSERT'):
                    continue
                line = line.replace('NULL', "''")
                for pid, title in regex.findall(line):
                    try:
                        rpid2pid[pid] = title2id[DataHandler.unescape_mysql(title)]
                    except KeyError:
                        print(pid, title)
                        # pdb.set_trace()
        return rpid2pid

    def get_redirecsfromXML(self, dump_date):
        db = MySQLDatabase(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
        conn = db._create_connection()
        df = pd.read_sql(('select * from redirects'),conn)
        return df.set_index('source_article_name')['target_article_name'].to_dict()

    @decorators.Cached
    def get_rpid2pidviaTitles(self, dump_date):
        print('get_rpid2pid...')
        title2id = self.get_title2id(dump_date)
        rpid2pid = {}
        redirects = self.get_redirecsfromXML(dump_date)
        for article_from in redirects:
            try:
                rpid2pid[title2id[article_from.replace(' ', '_')]] = title2id[redirects[article_from.replace(' ', '_')]]
            except KeyError:
                pass
        return rpid2pid

    @decorators.Cached
    def get_article2outlinks(self, clickstream_date):
        print('get_article2outlinks...')
        article2outlinks = collections.defaultdict(set)
        fname = '/home/ddimitrov/data/enwiki20150304_plus_clickstream/' + clickstream_date + '_clickstream.tsv'
        regex = re.compile(r'^([\d]+)\t([\d]+)')
        with open(fname) as infile:
            for lindex, line in enumerate(infile):
                if (lindex % 10000) == 0:
                    print('\r', lindex, end='')
                line = line.decode('utf-8')
                for left, right in regex.findall(line):
                    article2outlinks[int(left)].add(int(right))
        print()
        return article2outlinks

    def check_redirect_occurrences(self, dump_date, clickstream_date):
        print('check_redirect_occurrences...')
        article2outlinks = dh.get_article2outlinks(clickstream_date=clickstream_date)
        #rpid2pid = dh.get_rpid2pid(dump_date=dump_date)
        rpid2pid = dh.get_rpid2pidviaTitles(dump_date=dump_date)
        rpids_set = set(rpid2pid.keys())
        e = next(iter(rpids_set))
        print(type(e))
        links = []
        articles_keys_set = set(article2outlinks.keys())
        e = next(iter(articles_keys_set))
        print(type(e))
        e = next(iter(article2outlinks[e]))
        print(type(e))
        for aidx, article in enumerate(article2outlinks):
            if (aidx % 1000) == 0:
                print('\r', aidx+1, '/', len(article2outlinks), end='')
            intersection = article2outlinks[article] & rpids_set
            if len(intersection) > 0:
                print(len(intersection))
            for rpid in intersection:
                if rpid2pid[rpid] in article2outlinks[article]:
                    links.append((article, rpid, rpid2pid[rpid]))
        #pdb.set_trace()
        #self.write_results(dump_date, clickstream_date)
        fname = 'redirects_results_v' + str(dump_date) + '.csv'
        self.write_pickle(HOME+'output/'+fname, links)

    def read_pickle(self, fpath):
        with open(fpath, 'rb') as infile:
            obj = pickle.load(infile)
        return obj



if __name__ == '__main__':
    dump_date, clickstream_date = '20150304', '2015_02'
    #dump_date, clickstream_date = '20160305', '2016_02'

    dh = DataHandler()
    # title2id = dh.get_title2id(dump_date=dump_date)
    # rpid2pid = dh.get_rpid2pid(dump_date=dump_date)
    # article2outlinks = dh.get_article2outlinks(clickstream_date=clickstream_date)
    dh.check_redirect_occurrences(dump_date=dump_date, clickstream_date=clickstream_date)
    #fname = 'redirects_results_v' + str(dump_date) + '.csv'
    #obj = dh.read_pickle(HOME+'output/'+fname)
    #print (obj)
