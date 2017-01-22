import os
import os.path
from conf import *
import cPickle as pickle
from wsd.database import MySQLDatabase
import pandas as pn
import MySQLdb


def pickle_redirects_ids():
    db = MySQLDatabase(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
    db_work_view = db.get_work_view()

    redirects_list_id = []
    with open(HOME+"data/candidate_articles.tsv") as f:
        next(f)
        for line in f:
            line = line.strip().split('\t')
            #look up id
            tmp = db_work_view.resolve_title(line[0].replace('_',' '))
            #print tmp
            if tmp is not None:
               redirects_list_id.append(tmp['id'])
    pickle.dump(redirects_list_id, open(SSD_HOME+"pickle/redirects_ids.obj", "wb"), protocol=pickle.HIGHEST_PROTOCOL)




def export_data_unresolved():

    db = MySQLDatabase(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
    db_work_view = db.get_work_view()
    connection = db_work_view._db_connection


    df_clickstream = pn.read_csv('/home/ddimitrov/data/enwiki201608_unresolved_redirects/2016_08_clickstream_unresolved.tsv', sep='\t', error_bad_lines=False)

    df_clickstream['prev']=df_clickstream['prev'].str.replace('_', ' ')
    df_clickstream['curr']=df_clickstream['curr'].str.replace('_', ' ')
    df_clickstream['curr_unresolved']=df_clickstream['curr_unresolved'].str.replace('_', ' ')


    df_redirects_candidates = pn.read_sql('select * from redirects_candidates_sample', connection)


    sample_unresoleved = pn.merge(df_redirects_candidates, df_clickstream, how='left', left_on= ['source_article_name','target_article_name'], right_on=['prev', 'curr_unresolved'])

    sample_unresoleved['n'].fillna(0, inplace=True)
    sample_unresoleved.to_csv('/home/ddimitrov/data/enwiki201608_unresolved_redirects/data_unresolved.tsv', sep='\t',encoding="utf-8")



if __name__ == '__main__':
    #pickle_redirects_ids()
    export_data_unresolved()