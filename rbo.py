import numpy as np
import numpy.random
import matplotlib.pyplot as plt
import cPickle as pickle
import MySQLdb
from wsd.database import MySQLDatabase
import matplotlib.cm as cm
from matplotlib.colors import LogNorm, Normalize, BoundaryNorm, PowerNorm
from conf import *
__author__ = 'dimitrovdr'

from matplotlib import style
style.use('acm-3col')

import pylab
params = {
          'font.family' : 'serif',
          'font.serif' : ['Times New Roman'],
          'font.size' : 7
}
pylab.rcParams.update(params)

def rbo():
    print 'loading'
    db = MySQLDatabase(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
    conn = db._create_connection()
    cursor = conn.cursor()
    sm = []
    try:
        cursor.execute('select curr_id, sum(counts) as counts_sum, curr_title from clickstream_derived where link_type_derived=%s group by curr_id order by counts_sum desc limit 10000;', ("entry-sm",))
        result = cursor.fetchall()
        for row in result:
            record = {}
            record['curr_id']= row[0]
            record['counts_sum'] = row[1]
            record['curr_title'] = row[2]
            sm.append(row[0])
    except MySQLdb.Error, e:
        print e
		
    se = []
    try:
        cursor.execute('select curr_id, sum(counts) as counts_sum, curr_title from clickstream_derived where link_type_derived=%s group by curr_id order by counts_sum desc limit 10000;', ("entry-se",))
        result = cursor.fetchall()
        for row in result:
            record = {}
            record['curr_id']= row[0]
            record['counts_sum'] = row[1]
            record['curr_title'] = row[2]
            se.append(row[0])
    except MySQLdb.Error, e:
        print e
		
    p=0.9
    rbo_i = 0
    for i,e in enumerate(se, 1):
        se_i = se[:i]
        #print se_i
        sm_i = sm[:i]
        #print sm_i
        intersection_i = set(se_i).intersection(set(sm_i))
        #print intersection_i
        #print len(intersection_i)
        rbo_i += (2.0*len(intersection_i)/(len(se_i)+len(sm_i)))*p**(i-1)
    rbo = (1-p)*rbo_i
    print rbo
if __name__ == '__main__':
    rbo()
    
