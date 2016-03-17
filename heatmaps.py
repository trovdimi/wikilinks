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

def clicks_heatmap():
    print 'loading'
    db = MySQLDatabase(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
    db_worker_view = db.get_work_view()
    coords = db_worker_view.retrieve_all_links_coords_clicks()
    print 'coord loaded'
    links = {}
    x = []
    y = []
    values = []
    confident_values = []
    not_confident_values = []
    x_conf = []
    y_conf = []
    x_not_conf = []
    y_not_conf = []
    number_of_not_confident_clicks=0
    number_of_confident_clicks = 0
    number_of_valid_normed_links=0
    for coord in coords:
        try:
            v = links[coord['key']]
            links[coord['key']]+=1
        except:
            links[coord['key']]=0
    for coord in coords:
        x_normed = float(coord['x'])/float(1920)
        y_normed = float(coord['y'])/float(coord['page_length'])
        if  x_normed <=1.0 and y_normed <=1.0:
            x.append(x_normed)
            y.append(y_normed)
            number_of_valid_normed_links+=1
            if links[coord['key']]==0:
                x_conf.append(x_normed)
                y_conf.append(y_normed)
                values.append(float(coord['counts']))
                number_of_confident_clicks+=1
                confident_values.append(coord['counts'])
            else:
                x_not_conf.append(x_normed)
                y_not_conf.append(y_normed)
                values.append(float(coord['counts'])/float(links[coord['key']])+1.0)
                number_of_not_confident_clicks+=1
                not_confident_values.append(float(coord['counts'])/float(links[coord['key']]))
    print '###########'
    print sum(values)
    print sum(confident_values)
    print number_of_confident_clicks
    print sum(not_confident_values)
    print number_of_not_confident_clicks
    print number_of_valid_normed_links
    print len(coords)
    print '###########'



    heatmap, xedges, yedges = np.histogram2d(x_conf, y_conf, bins=100, weights=confident_values)
    extent = [xedges[0], xedges[-1], yedges[-1], yedges[0] ]

    fig_size = (2.4, 2)
    #fig_size = (3.5, 3)
    plt.clf()
    plt.figure(figsize=fig_size)

    plt.grid(True)
    plt.imshow(heatmap, extent=extent, origin='upper', norm=LogNorm(), cmap=plt.get_cmap('jet'))
    plt.colorbar()
    #plt.title("Clicks Heatmap Log Normalized")

    plt.show()
    plt.savefig('output/clicks_heatmap_lognormed_self_loop_confident.pdf')

    plt.clf()
    plt.figure(figsize=fig_size)

    plt.grid(True)
    plt.imshow(heatmap , extent=extent, origin='upper', norm=Normalize(), cmap=plt.get_cmap('jet'))
    plt.colorbar()
    #plt.title("Clicks Heatmap Normalized")

    plt.show()
    plt.savefig('output/clicks_heatmap_normed_self_loop_confident.pdf')
    print "conf done"

    heatmap, xedges, yedges = np.histogram2d(x_not_conf, y_not_conf, bins=100, weights=not_confident_values)
    extent = [xedges[0], xedges[-1], yedges[-1], yedges[0] ]

    fig_size = (2.4, 2)
    #fig_size = (3.5, 3)
    plt.clf()
    plt.figure(figsize=fig_size)

    plt.grid(True)
    plt.imshow(heatmap, extent=extent, origin='upper', norm=LogNorm(), cmap=plt.get_cmap('jet'))
    plt.colorbar()
    #plt.title("Clicks Heatmap Log Normalized")

    plt.show()
    plt.savefig('output/clicks_heatmap_lognormed_self_loop_not_confident.pdf')

    plt.clf()
    plt.figure(figsize=fig_size)

    plt.grid(True)
    plt.imshow(heatmap , extent=extent, origin='upper', norm=Normalize(), cmap=plt.get_cmap('jet'))
    plt.colorbar()
    #plt.title("Clicks Heatmap Normalized")

    plt.show()
    plt.savefig('output/clicks_heatmap_normed_self_loop_not_confident.pdf')
    print " not conf done"


    heatmap, xedges, yedges = np.histogram2d(x, y, bins=100, weights=values)
    extent = [xedges[0], xedges[-1], yedges[-1], yedges[0] ]

    fig_size = (2.4, 2)
    #fig_size = (3.5, 3)
    plt.clf()
    plt.figure(figsize=fig_size)

    plt.grid(True)
    plt.imshow(heatmap, extent=extent, origin='upper', norm=LogNorm(), cmap=plt.get_cmap('jet'))
    plt.colorbar()
    #plt.title("Clicks Heatmap Log Normalized")

    plt.show()
    plt.savefig('output/clicks_heatmap_lognormed_self_loop_1.pdf')

    plt.clf()
    plt.figure(figsize=fig_size)

    plt.grid(True)
    plt.imshow(heatmap , extent=extent, origin='upper', norm=Normalize(), cmap=plt.get_cmap('jet'))
    plt.colorbar()
    #plt.title("Clicks Heatmap Normalized")

    plt.show()
    plt.savefig('output/clicks_heatmap_normed_self_loop_1.pdf')
    print "done"

def clicks_heatmap_first_occ():
    print 'loading'
    db = MySQLDatabase(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
    db_worker_view = db.get_work_view()
    coords = db_worker_view.retrieve_all_links_coords_clicks_first_occ()
    print 'coord loaded'
    links = {}
    x = []
    y = []
    values = []
    for link in coords.values():
        x_normed = float(link['x'])/float(1920)
        y_normed = float(link['y'])/float(link['page_length'])
        if  x_normed <=1.0 and y_normed <=1.0:
            x.append(x_normed)
            y.append(y_normed)
            values.append(float(link['counts']))


    heatmap, xedges, yedges = np.histogram2d(x, y, bins=100, weights=values)
    extent = [xedges[0], xedges[-1], yedges[-1], yedges[0] ]

    fig_size = (2.4, 2)

    plt.clf()
    plt.figure(figsize=fig_size)

    plt.grid(True)
    plt.imshow(heatmap , extent=extent, origin='upper', norm=LogNorm(), cmap=plt.get_cmap('jet'))
    plt.colorbar()
    #plt.title("Clicks Heatmap Log Normalized")

    plt.show()
    plt.savefig('output/clicks_heatmap_lognormed_self_loop_first_occ.pdf')

    plt.clf()
    plt.figure(figsize=fig_size)

    plt.grid(True)
    plt.imshow(heatmap , extent=extent, origin='upper', norm=Normalize(), cmap=plt.get_cmap('jet'))
    plt.colorbar()
    #plt.title("Clicks Heatmap Normalized")

    plt.show()
    plt.savefig('output/clicks_heatmap_normed_self_loop_first_occ.pdf')
    print "done"

def clicks_heatmap_total():
    print 'loading'
    db = MySQLDatabase(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
    db_worker_view = db.get_work_view()
    coords = db_worker_view.retrieve_all_links_coords_clicks()
    print 'coord loaded'
    links = {}
    x = []
    y = []
    values = []
    for coord in coords:
        x_normed = float(coord['x'])/float(1920)
        y_normed = float(coord['y'])/float(coord['page_length'])
        if x_normed <=1.0 and y_normed <=1.0:
            x.append(x_normed)
            y.append(y_normed)
            values.append(float(coord['counts']))

    heatmap, xedges, yedges = np.histogram2d(x, y, bins=100, weights=values)
    extent = [xedges[0], xedges[-1], yedges[-1], yedges[0] ]


    fig_size = (2.4, 2)

    plt.clf()
    plt.figure(figsize=fig_size)

    plt.grid(True)
    plt.imshow(heatmap , extent=extent, origin='upper', norm=LogNorm(), cmap=plt.get_cmap('jet'))
    plt.colorbar()
    #plt.title("Clicks Heatmap Log Normalized")

    plt.show()
    plt.savefig('output/clicks_heatmap_lognormed_self_loop_total.pdf')

    plt.clf()
    plt.figure(figsize=fig_size)

    plt.grid(True)
    plt.imshow(heatmap , extent=extent, origin='upper', norm=Normalize(), cmap=plt.get_cmap('jet'))
    plt.colorbar()
    #plt.title("Clicks Heatmap Normalized")

    plt.show()
    plt.savefig('output/clicks_heatmap_normed_self_loop_total.pdf')
    print "done"


def links_heatmap():
    #http://stackoverflow.com/questions/2369492/generate-a-heatmap-in-matplotlib-using-a-scatter-data-set
    # Get URLs from a text file, remove white space.
    print 'loading'
    db = MySQLDatabase(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
    db_worker_view = db.get_work_view()
    coords = db_worker_view.retrieve_all_links_coords()
    print 'coord loaded'
    x=[]
    y=[]

    page_lenghts = db_worker_view.retrieve_all_page_lengths()
    print 'lenghts loaded'
    for coord in coords:
        x_normed = float(coord['x'])/float(1920)
        y_normed = float(coord['y'])/float(page_lenghts[coord['source_article_id']])
        if  x_normed <=1.0 and y_normed <=1.0:
            x.append(x_normed)
            y.append(y_normed)



    heatmap, xedges, yedges = np.histogram2d(x, y, bins=100)
    extent = [xedges[0], xedges[-1], yedges[-1], yedges[0]]

    fig_size = (2.4, 2)
    #fig_size = (3.5, 3)
    plt.clf()
    plt.figure(figsize=fig_size)
    plt.grid(True)

    plt.imshow(heatmap, extent=extent, origin='upper', norm=LogNorm(), cmap=plt.get_cmap('jet'))
    plt.colorbar()
    #plt.title("Links Heatmap Log Normalized")

    plt.show()
    plt.savefig('output/links_heatmap_lognormed_self_loop.pdf')

    plt.clf()
    plt.figure(figsize=fig_size)
    plt.grid(True)

    plt.imshow(heatmap , extent=extent, origin='upper', norm=Normalize(),cmap=plt.get_cmap('jet'))
    plt.colorbar()
    #plt.title("Links Heatmap Normalized")

    plt.show()
    plt.savefig('output/links_heatmap_normed_self_loop.pdf')

    print "done"


def multiple_links_heatmap():
    print 'loading'
    db = MySQLDatabase(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
    db_worker_view = db.get_work_view()
    coords = db_worker_view.retrieve_all_links_multpile_occ()
    print 'coord loaded'
    page_lenghts = db_worker_view.retrieve_all_page_lengths()
    print 'lenghts loaded'
    links = {}
    x = []
    y = []
    x_conf = []
    y_conf = []
    x_not_conf = []
    y_not_conf = []
    number_of_not_confident_clicks=0
    number_of_confident_clicks = 0
    number_of_valid_normed_links=0
    for coord in coords:
        try:
            v = links[coord['key']]
            links[coord['key']]+=1
        except:
            links[coord['key']]=0
    for coord in coords:
        x_normed = float(coord['x'])/float(1920)
        y_normed = float(coord['y'])/float(page_lenghts[coord['key'][0]])
        if  x_normed <=1.0 and y_normed <=1.0:
            x.append(x_normed)
            y.append(y_normed)
            number_of_valid_normed_links+=1
            if links[coord['key']]==0:
                x_conf.append(x_normed)
                y_conf.append(y_normed)
                number_of_confident_clicks+=1
            else:
                x_not_conf.append(x_normed)
                y_not_conf.append(y_normed)
                number_of_not_confident_clicks+=1
    print '###########'
    print number_of_confident_clicks
    print number_of_not_confident_clicks
    print number_of_valid_normed_links
    print len(coords)
    print '###########'



    heatmap, xedges, yedges = np.histogram2d(x_conf, y_conf, bins=100)
    extent = [xedges[0], xedges[-1], yedges[-1], yedges[0]]

    fig_size = (2.4, 2)
    #fig_size = (3.5, 3)
    plt.clf()
    plt.figure(figsize=fig_size)
    plt.grid(True)

    plt.imshow(heatmap, extent=extent, origin='upper', norm=LogNorm(), cmap=plt.get_cmap('jet'))
    plt.colorbar()
    #plt.title("Links Heatmap Log Normalized")

    plt.show()
    plt.savefig('output/links_heatmap_lognormed_self_loop_unique.pdf')

    plt.clf()
    plt.figure(figsize=fig_size)
    plt.grid(True)

    plt.imshow(heatmap , extent=extent, origin='upper', norm=Normalize(),cmap=plt.get_cmap('jet'))
    plt.colorbar()
    #plt.title("Links Heatmap Normalized")

    plt.show()
    plt.savefig('output/links_heatmap_normed_self_loop_unique.pdf')

    print "unique done"

    heatmap, xedges, yedges = np.histogram2d(x_not_conf, y_not_conf, bins=100)
    extent = [xedges[0], xedges[-1], yedges[-1], yedges[0]]

    fig_size = (2.4, 2)
    #fig_size = (3.5, 3)
    plt.clf()
    plt.figure(figsize=fig_size)
    plt.grid(True)

    plt.imshow(heatmap, extent=extent, origin='upper', norm=LogNorm(), cmap=plt.get_cmap('jet'))
    plt.colorbar()
    #plt.title("Links Heatmap Log Normalized")

    plt.show()
    plt.savefig('output/links_heatmap_lognormed_self_loop_multiple.pdf')

    plt.clf()
    plt.figure(figsize=fig_size)
    plt.grid(True)

    plt.imshow(heatmap , extent=extent, origin='upper', norm=Normalize(),cmap=plt.get_cmap('jet'))
    plt.colorbar()
    #plt.title("Links Heatmap Normalized")

    plt.show()
    plt.savefig('output/links_heatmap_normed_self_loop_multiple.pdf')

    print "done"


def links_heatmap_rel_prob():
    #http://stackoverflow.com/questions/2369492/generate-a-heatmap-in-matplotlib-using-a-scatter-data-set
    # Get URLs from a text file, remove white space.
    print 'loading'
    db = MySQLDatabase(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
    db_worker_view = db.get_work_view()
    coords = db_worker_view.retrieve_all_links_coords()

    x=[]
    y=[]


    page_lenghts = db_worker_view.retrieve_all_page_lengths()

    for coord in coords:
        x_normed = float(coord['x'])/float(1920)
        y_normed = float(coord['y'])/float(page_lenghts[coord['source_article_id']])
        if  x_normed <=1.0 and y_normed <=1.0:
            x.append(x_normed)
            y.append(y_normed)



    links_heatmap_hist, xedges, yedges = np.histogram2d(x, y, normed=True,  bins=100)
    links_extent = [xedges[0], xedges[-1], yedges[-1], yedges[0]]




    coords = db_worker_view.retrieve_all_links_coords_clicks()
    print 'coord loaded'
    links = {}
    x = []
    y = []
    values = []
    for coord in coords:
       try:
           v = links[coord['key']]
           links[coord['key']]+=1
       except:
           links[coord['key']]=0
    for coord in coords:
       x_normed = float(coord['x'])/float(1920)
       y_normed = float(coord['y'])/float(coord['page_length'])
       if  x_normed <=1.0 and y_normed <=1.0:
           x.append(x_normed)
           y.append(y_normed)
           if links[coord['key']]==0:
	       #x.append(x_normed)
               #y.append(y_normed)
               values.append(float(coord['counts']))
           else:
               values.append(float(coord['counts'])/float(links[coord['key']]))

    clicks_heatmap_hist, xedges, yedges = np.histogram2d(x, y, bins=100, normed=True, weights=values)
    clicks_extent = [xedges[0], xedges[-1], yedges[-1], yedges[0]]

    substraction_hist = np.subtract(clicks_heatmap_hist,links_heatmap_hist)
    #rel_prob_hist = np.divide(clicks_heatmap_hist, links_heatmap_hist)
    with np.errstate(divide='ignore', invalid='ignore'):
        rel_prob_hist = np.divide(clicks_heatmap_hist, links_heatmap_hist)
        rel_prob_hist[rel_prob_hist == np.inf] = 0
        rel_prob_hist = np.nan_to_num(rel_prob_hist)

    fig_size = (2.4, 2)

    plt.clf()
    plt.figure(figsize=fig_size)
    plt.grid(True)

    plt.imshow(substraction_hist, extent=clicks_extent, origin='upper',norm=Normalize(), cmap=plt.get_cmap('jet'))
    plt.colorbar()


    plt.show()
    plt.savefig('output/clicks-links_heatmap_normed_self_loop.pdf')


    plt.clf()
    plt.figure(figsize=fig_size)
    plt.grid(True)

    plt.imshow(rel_prob_hist , extent=clicks_extent, origin='upper', norm=Normalize(),cmap=plt.get_cmap('jet'))
    plt.colorbar()


    plt.show()
    plt.savefig('output/clicks_over_links_heatmap_normed_self_loop.pdf')


    plt.clf()
    plt.figure(figsize=fig_size)
    plt.grid(True)

    plt.imshow(substraction_hist, extent=clicks_extent, origin='upper', norm=LogNorm(), cmap=plt.get_cmap('jet'))
    plt.colorbar()


    plt.show()
    plt.savefig('output/clicks-links_heatmap_lognormed_self_loop.pdf')


    plt.clf()
    plt.figure(figsize=fig_size)
    plt.grid(True)

    plt.imshow(rel_prob_hist , extent=clicks_extent, origin='upper', norm=LogNorm(), cmap=plt.get_cmap('jet'))
    plt.colorbar()


    plt.show()
    plt.savefig('output/clicks_over_links_heatmap_lognormed_self_loop.pdf')


    substraction_hist = np.subtract(links_heatmap_hist, clicks_heatmap_hist)
    #rel_prob_hist = np.divide(clicks_heatmap_hist, links_heatmap_hist)
    with np.errstate(divide='ignore', invalid='ignore'):
        rel_prob_hist = np.divide(links_heatmap_hist, clicks_heatmap_hist)
        rel_prob_hist[rel_prob_hist == np.inf] = 0
        rel_prob_hist = np.nan_to_num(rel_prob_hist)



    plt.clf()
    plt.figure(figsize=fig_size)
    plt.grid(True)

    plt.imshow(substraction_hist, extent=clicks_extent, origin='upper', norm=Normalize(), cmap=plt.get_cmap('jet'))
    plt.colorbar()
    #plt.title("Links Heatmap Normalized")

    plt.show()
    plt.savefig('output/links-clicks_heatmap_normed_self_loop.pdf')


    plt.clf()
    plt.figure(figsize=fig_size)
    plt.grid(True)

    plt.imshow(rel_prob_hist , extent=clicks_extent, origin='upper', norm=Normalize(), cmap=plt.get_cmap('jet'))
    plt.colorbar()
    #plt.title("Links Heatmap Normalized")

    plt.show()
    plt.savefig('output/links_over_clicks_heatmap_normed_self_loop.pdf')

    plt.clf()
    plt.figure(figsize=fig_size)
    plt.grid(True)

    plt.imshow(substraction_hist, extent=clicks_extent, origin='upper', norm=LogNorm(), cmap=plt.get_cmap('jet'))
    plt.colorbar()
    #plt.title("Links Heatmap Normalized")

    plt.show()
    plt.savefig('output/links-clicks_heatmap_lognormed_self_loop.pdf')


    plt.clf()
    plt.figure(figsize=fig_size)
    plt.grid(True)

    plt.imshow(rel_prob_hist , extent=clicks_extent, origin='upper', norm=LogNorm(), cmap=plt.get_cmap('jet'))
    plt.colorbar()
    #plt.title("Links Heatmap Normalized")

    plt.show()
    plt.savefig('output/links_over_clicks_heatmap_lognormed_self_loop.pdf')
    print "done"



if __name__ == '__main__':
    links_heatmap()
    clicks_heatmap_first_occ()
    clicks_heatmap_total()
    clicks_heatmap()
    multiple_links_heatmap()
    links_heatmap_rel_prob()
