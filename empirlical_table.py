from wsd.database import MySQLDatabase
from conf import *
import MySQLdb
import cPickle as pickle
import numpy as np
import pandas as pd

__author__ = 'dimitrovdr'



def resultTableLine (df, description, feature, sep="\t"):
    s = description + sep
    s += "{:,}".format(int(df[eval(feature)]['counts'].count())) + sep
    s += "{:,}".format(int(df[eval(feature)]['counts'].sum())) + sep
    s += "{0:.2f}".format(df[eval(feature)]['counts'].sum() / df[eval(feature)]['counts'].count()) + "\n"
    return s


def print_table():
    db = MySQLDatabase(DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, DATABASE_NAME)
    conn = db._create_connection()

    df = pd.read_sql('select source_article_id, target_article_id, rel_degree, rel_in_degree, rel_out_degree, '
                     'rel_page_rank, rel_kcore, target_x_coord_1920_1080, target_y_coord_1920_1080, visual_region, '
                     'IFNULL(counts, 0) as counts from link_features order by source_article_id, target_y_coord_1920_1080, target_x_coord_1920_1080', conn)

    print "dup"
    #no_dup = df.sort(['source_article_id','target_y_coord_1920_1080','target_x_coord_1920_1080']).groupby(["source_article_id", "target_article_id"]).first()
    no_dup = df.groupby(["source_article_id", "target_article_id"]).first()

    no_dup = no_dup.reset_index()
    print "no dup"
    del df
    #print no_dup
    df_top = pd.read_sql("select source_article_id, target_article_id, sim as topic_similarity  from topic_similarity", conn)
    print "no up"
    topDF = df_top.groupby("source_article_id", as_index=False)["topic_similarity"].median()
    #print topDF
    print "no up1"
    topDF.columns = ["source_article_id", "topic_similarity_article_median"]
    #print topDF
    print "no up2"
    df_top = df_top.merge(topDF, on="source_article_id")
    #print df_top[(df_top['topic_similarity_article_median'] >0)]
    print "no up3"

    df_sem = pd.read_sql("select source_article_id, target_article_id, sim as sem_similarity from semantic_similarity", conn)
    print "no up4"
    semDF = df_sem.groupby("source_article_id", as_index=False)["sem_similarity"].median()
    #rename
    print "no up5"
    semDF.columns = ["source_article_id", "sem_similarity_article_median"]
    print "no up6"
    #print df_top
    df_sem = df_sem.merge(semDF, on="source_article_id")
    #print len(df_sem)
    print "no up7"
    df1 = no_dup.merge(df_sem[['source_article_id', 'sem_similarity', 'sem_similarity_article_median']], on="source_article_id")
    #print no_dup
    del df_sem, semDF
    df = no_dup.merge(df_top[['source_article_id', 'topic_similarity', 'topic_similarity_article_median']], on="source_article_id")
    print "no up9"
    del no_dup
    del df_top, topDF

    table = ""

    table += resultTableLine (df, "src_degr > target_degr", "df.rel_degree > 0")
    table += resultTableLine (df, "src_degr <= target_degr", "df.rel_degree <= 0")


    table += resultTableLine (df, "src_in_degr > target_in_degr", "df.rel_in_degree > 0")
    table += resultTableLine (df, "src_in_degr <= target_in_degr", "df.rel_in_degree <= 0")


    table += resultTableLine (df, "src_out_degr > target_out_degr", "df.rel_out_degree > 0")
    table += resultTableLine (df, "src_out_degr <= target_out_degr", "df.rel_out_degree <= 0")

    table += resultTableLine (df, "src_kcore > target_kcore", "df.rel_kcore > 0")
    table += resultTableLine (df, "src_kcore <= target_kcore", "df.rel_kcore <= 0")

    table += resultTableLine (df, "src_page_rank > target_page_rank", "df.rel_page_rank > 0")
    table += resultTableLine (df, "src_page_rank <= target_page_rank", "df.rel_page_rank <= 0")


    table += resultTableLine (df1, "text_sim > median(text_sim) of page", "df.sem_similarity > df.sem_similarity_article_median")
    table += resultTableLine (df1, "text_sim <= median(text_sim) of page", "df.sem_similarity <= df.sem_similarity_article_median")

    table += resultTableLine (df, "topic_sim > median(topic_sim) of page", "df.topic_similarity > df.topic_similarity_article_median")
    table += resultTableLine (df, "topic_sim <= median(topic_sim) of page", "df.topic_similarity <= df.topic_similarity_article_median")


    table += resultTableLine (df, "left third of screen", "df.target_x_coord_1920_1080 <= 360")
    table += resultTableLine (df, "middle third of screen", "(df.target_x_coord_1920_1080 > 360) & (df.target_x_coord_1920_1080 <= 720)")
    table += resultTableLine (df, "right third of screen", "df.target_x_coord_1920_1080 > 720")

    table += resultTableLine (df, "position = lead", "df.visual_region == 'lead'")
    table += resultTableLine (df, "position = body", "(df.visual_region == 'body') | (df.visual_region == 'left-body')")
    table += resultTableLine (df, "position = navbox", "df.visual_region == 'navbox'")
    #table += resultTableLine (df, "position = left-body", "df.visual_region == 'left-body'")
    table += resultTableLine (df, "position = infobox", "df.visual_region == 'infobox'")


    print table


if __name__ == '__main__':
    print_table()

