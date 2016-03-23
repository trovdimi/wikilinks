import MySQLdb
import logging


class MySQLWorkView:
    """The MySQLWorkView class allows database access optimized to
       retrieve disambiguation entries from the database
    """

    def __init__(self, db_connection):
        """constructor

           @param db_connector the database connector used to access the database
        """
        self._db_connection = db_connection
        self._cursor = db_connection.cursor()
        self.reset_cache()

    def __del__(self):
        """destructor
           closes the database connection
        """
        self._db_connection.close()

    def reset_cache(self):
        """resets the internal cache and thus prevents it from growing too big
        """
        self._redirect_cache = {}
        self._link_cache = {}
        self._article_cache = {}
        self._occurrences_cache = {}
        self._templates_cache = {}

    def resolve_redirect(self, name):
        """resolves a redirect and returns the real article name

           @param name the name of the redirect
           
           @return the real name of the article or None if it cannot be resolved
        """
        try:
            self._cursor.execute('SELECT target_article_name FROM redirects WHERE source_article_name=%s;', (name,))
            row = self._cursor.fetchone()
            if row != None:
                return row[0]
        except MySQLdb.Error, e:
            logging.error('error resolving redirect for name "%s": %s (%d)'
                          % (name.encode('ascii', 'ignore'), e.args[1], e.args[0]))
        return None

    def retrieve_number_of_common_articles(self, id1, id2):
        """computes the number of articles that link to both referenced articles

            @param id1 the id of the first article to be linked to
            @param id2 the id of the second article to be linked to

            @return the number of articles that link to both referenced articles
        """
        # retrieve from database and store in cache
        try:
            if id1 not in self._link_cache:
                self._cursor.execute('SELECT source_article_id FROM links WHERE target_article_id=%s;', (id1,))
                self._link_cache[id1] = self._cursor.fetchall()
            if id2 not in self._link_cache:
                self._cursor.execute('SELECT source_article_id FROM links WHERE target_article_id=%s;', (id2,))
                self._link_cache[id2] = self._cursor.fetchall()
        except MySQLdb.Error, e:
            logging.error('error resolving links for source article id %d or %d: %s (%d)'
                          % (id1, id2, e.args[1], e.args[0]))

        # find common articles
        counter = 0
        for source1 in self._link_cache[id1]:
            for source2 in self._link_cache[id2]:
                if source1 == source2:
                    counter += 1

        return counter


    def resolve_title(self, title):
        """resolves an article and returns it

           @param title the title of the article

           @return a dictionary with fields 'id' and 'title' or None if could not be resolved
        """
        if title in self._article_cache:
            return self._article_cache[title]

        try:
            t = title[0].upper() + title[1:]
            self._cursor.execute('SELECT id, title FROM articles WHERE title=%s;', (t,))
            row = self._cursor.fetchone()
            if row == None:
                self._cursor.execute(
                    'SELECT id, title FROM articles WHERE title=(SELECT target_article_name FROM redirects WHERE source_article_name=%s);',
                    (title,))
                row = self._cursor.fetchone()

            if row == None:
                print t
                self._article_cache[title] = None
            else:
                self._article_cache[title] = {'id': row[0], 'title': row[1]}
                if (row[1] != title):
                    self._article_cache[row[1]] = {'id': row[0], 'title': row[1]}
        except MySQLdb.Error, e:
            logging.error('error resolving article "%s": %s (%d)'
                          % (title.encode('ascii', 'ignore'), e.args[1], e.args[0]))

        if title in self._article_cache:
            return self._article_cache[title]
        return None





    def retrieve_all_articles(self):
        """retrieves all articles. useful for crawling or making media wiki api requests
        @return a list of dictionaries holding the following keys:
           'id': the id of the retrieved article
           'rev_id': the revision id  of the retrieved article
           'title': the title of the retrieved article
                """
        articles = []
        try:
            #self._cursor.execute('SELECT * FROM articles WHERE RAND()<=0.0006 limit 1000;')
            #self._cursor.execute('SELECT * FROM articles limit 1000;')
            self._cursor.execute('SELECT * FROM articles;')
            result = self._cursor.fetchall()
            for row in result:
                article = {}
                article['id'] = row[0]
                article['rev_id'] = row[1]
                article['title'] = row[2]
                articles.append(article)
        except MySQLdb.Error, e:
            logging.error('error retrieving 1000 random articles  %s (%d)' % (e.args[1], e.args[0]))
        return articles


    def retrieve_all_articles_questionmark(self):
            """retrieves all articles. useful for crawling or making media wiki api requests
            @return a list of dictionaries holding the following keys:
               'id': the id of the retrieved article
               'rev_id': the revision id  of the retrieved article
               'title': the title of the retrieved article
                    """
            articles = []
            try:
                #self._cursor.execute('SELECT * FROM articles WHERE RAND()<=0.0006 limit 1000;')
                #self._cursor.execute('SELECT * FROM articles limit 1000;')
                self._cursor.execute('SELECT * FROM articles WHERE title LIKE %s;', ("?%",))
                result = self._cursor.fetchall()
                for row in result:
                    article = {}
                    article['id'] = row[0]
                    article['rev_id'] = row[1]
                    article['title'] = row[2]
                    articles.append(article)
            except MySQLdb.Error, e:
                logging.error('error retrieving 1000 random articles  %s (%d)' % (e.args[1], e.args[0]))
            return articles


    def retrieve_all_unique_links(self):
            """retrieves all links. These are the network edges
            @return a list of dictionaries holding the following keys:
               'from': the source article id
               'to': the target article id
                    """
            links = []
            try:
                self._cursor.execute('SELECT * FROM unique_links;')
                result = self._cursor.fetchall()
                for row in result:
                    link = {}
                    link['from'] = row[0]
                    link['to'] = row[1]
                    links.append(link)
            except MySQLdb.Error, e:
                logging.error('error retrieving unique links %s (%d)' % (e.args[1], e.args[0]))
            return links

    def retrieve_all_transitions(self):
                """retrieves all transitions from the wikipeida clickstream_derived that are an internal links. These are the network edges
                @return a list of dictionaries holding the following keys:
                   'from': the source article id
                   'to': the target article id
                        """
                links = []
                try:
                    self._cursor.execute('SELECT * FROM clickstream_derived WHERE link_type_derived LIKE %s;', ("internal%",))
                    result = self._cursor.fetchall()
                    for row in result:
                        link = {}
                        link['from'] = row[0]
                        link['to'] = row[1]
                        links.append(link)
                except MySQLdb.Error, e:
                    logging.error('error retrieving unique links %s (%d)' % (e.args[1], e.args[0]))
                return links

    def retrieve_all_links_coords(self):
            """retrieves all xy coord for all links in wikipeida.
            @return a list of coords holding the following keys:
               'source_article_id': the wikipedia article id
               'x': x position on screen
               'y': y position on screen
                    """
            coords = []
            try:
                self._cursor.execute('SELECT source_article_id, target_x_coord_1920_1080, target_y_coord_1920_1080 FROM links where target_x_coord_1920_1080 is not Null and target_y_coord_1920_1080 is not Null and target_x_coord_1920_1080!=0 and target_y_coord_1920_1080!=0 and source_article_id!=target_article_id;')
                result = self._cursor.fetchall()
                for row in result:
                    link = {}
                    link['source_article_id']= row[0]
                    link['x'] = row[1]
                    link['y'] = row[2]
                    coords.append(link)
            except MySQLdb.Error, e:
                logging.error('error retrieving xy coord for all links links %s (%d)' % (e.args[1], e.args[0]))
            return coords

    def retrieve_all_page_lengths(self):
                """retrieves all page lengths.
                @return a dict of lengths holding the following keys:
                   'id': the lenght of the page with the id
                """
                pages = {}
                try:
                    self._cursor.execute('SELECT *  FROM page_length;')
                    result = self._cursor.fetchall()
                    for row in result:
                        pages[row[0]]=row[1]
                except MySQLdb.Error, e:
                    logging.error('error retrieving pagelength: %s (%d)' % (e.args[1], e.args[0]))
                return pages

    def retrieve_all_links_coords_clicks(self):
        """retrieves all xy coord for all links in wikipeida.
        @return a list of coords holding the following keys:
           'source_article_id': the wikipedia article id
           'x': x position on screen
           'y': y position on screen
                """
        coords = []
        try:
            self._cursor.execute('select l.source_article_id, l.target_article_id, l.target_x_coord_1920_1080, l.target_y_coord_1920_1080, c.counts, p.page_length_1920_1080 from links l, clickstream_derived c, page_length p where l.source_article_id=c.prev_id and l.target_article_id=c.curr_id and c.link_type_derived like %s and l.source_article_id = p.id and l.target_x_coord_1920_1080 is not Null and l.target_y_coord_1920_1080 is not Null  and l.target_x_coord_1920_1080!=0 and l.target_y_coord_1920_1080!=0  and l.source_article_id!=l.target_article_id;', ("internal%",))
            result = self._cursor.fetchall()
            for row in result:
                link = {}
                link['key']= row[0], row[1]
                link['x'] = row[2]
                link['y'] = row[3]
                link['counts'] = row[4]
                link['page_length'] = row[5]
                coords.append(link)
        except MySQLdb.Error, e:
            logging.error('error retrieving xy coord for all links links %s (%d)' % (e.args[1], e.args[0]))
        return coords

    def retrieve_all_links_multpile_occ(self):
        """retrieves all xy coord for all links in wikipeida.
        @return a list of coords holding the following keys:
           'source_article_id': the wikipedia article id
           'x': x position on screen
           'y': y position on screen
                """
        coords = []
        try:
            self._cursor.execute('SELECT source_article_id, target_article_id, target_x_coord_1920_1080, target_y_coord_1920_1080 FROM links where target_x_coord_1920_1080 is not Null and target_y_coord_1920_1080 is not Null and target_x_coord_1920_1080!=0 and target_y_coord_1920_1080!=0 and source_article_id!=target_article_id;')
            result = self._cursor.fetchall()
            for row in result:
                link = {}
                link['key']= row[0], row[1]
                link['x'] = row[2]
                link['y'] = row[3]
                coords.append(link)
        except MySQLdb.Error, e:
            logging.error('error retrieving xy coord for all links links %s (%d)' % (e.args[1], e.args[0]))
        return coords

    def retrieve_all_links_coords_clicks_first_occ(self):
        """retrieves all xy coord for all links in wikipeida.
        @return a list of coords holding the following keys:
           'source_article_id': the wikipedia article id
           'x': x position on screen
           'y': y position on screen
                """
        links = {}
        try:
            self._cursor.execute('select l.source_article_id, l.target_article_id, l.target_x_coord_1920_1080, l.target_y_coord_1920_1080, c.counts, p.page_length_1920_1080 from links l, clickstream_derived c, page_length p where l.source_article_id=c.prev_id and l.target_article_id=c.curr_id and c.link_type_derived like %s and l.source_article_id = p.id and l.target_x_coord_1920_1080 is not Null and l.target_y_coord_1920_1080 is not Null and l.target_x_coord_1920_1080!=0 and l.target_y_coord_1920_1080!=0 and l.source_article_id!=l.target_article_id;', ("internal%",))
            result = self._cursor.fetchall()
            for row in result:
                link = {}
                link['x'] = row[2]
                link['y'] = row[3]
                link['counts'] = row[4]
                link['page_length'] = row[5]
                try:
                    prev = links[row[0], row[1]]
                    if prev['y'] > link['y']:
                        links[row[0], row[1]] = link
                    if prev['y']==link['y']:
                        if prev['x']>link['y']:
                            links[row[0], row[1]] = link
                except:
                    links[row[0], row[1]] = link
        except MySQLdb.Error, e:
            logging.error('error retrieving xy coord for all links links %s (%d)' % (e.args[1], e.args[0]))
        return links

    def retrieve_all_links_coords_page_rank(self):

        coords = []
        try:
            self._cursor.execute('select l.source_article_id, l.target_article_id, l.target_x_coord_1920_1080, l.target_y_coord_1920_1080, f.page_rank, p.page_length_1920_1080 from links l, article_features f, page_length p where l.target_article_id=f.id and  l.source_article_id = p.id and l.target_x_coord_1920_1080 is not Null and l.target_y_coord_1920_1080 is not Null  and l.target_x_coord_1920_1080!=0 and l.target_y_coord_1920_1080!=0;')
            result = self._cursor.fetchall()
            print 'result fetched'
            for row in result:
                link = {}
                link['key']= row[0], row[1]
                link['x'] = row[2]
                link['y'] = row[3]
                link['page_rank'] = row[4]
                link['page_length'] = row[5]
                coords.append(link)
        except MySQLdb.Error, e:
            logging.error('error retrieving xy coord for all links links %s (%d)' % (e.args[1], e.args[0]))
        return coords

    def retrieve_all_links_coords_indegree(self):

        coords = []
        try:
            self._cursor.execute('select l.source_article_id, l.target_article_id, l.target_x_coord_1920_1080, l.target_y_coord_1920_1080, f.in_degree, p.page_length_1920_1080 from links l, article_features f, page_length p where l.target_article_id=f.id and  l.source_article_id = p.id and l.target_x_coord_1920_1080 is not Null and l.target_y_coord_1920_1080 is not Null  and l.target_x_coord_1920_1080!=0 and l.target_y_coord_1920_1080!=0;')
            result = self._cursor.fetchall()
            for row in result:
                link = {}
                link['key']= row[0], row[1]
                link['x'] = row[2]
                link['y'] = row[3]
                link['in_degree'] = row[4]
                link['page_length'] = row[5]
                coords.append(link)
        except MySQLdb.Error, e:
            logging.error('error retrieving xy coord for all links links %s (%d)' % (e.args[1], e.args[0]))
        return coords

    def retrieve_all_links_coords_outdegree(self):

        coords = []
        try:
            self._cursor.execute('select l.source_article_id, l.target_article_id, l.target_x_coord_1920_1080, l.target_y_coord_1920_1080, f.out_degree, p.page_length_1920_1080 from links l, article_features f, page_length p where l.target_article_id=f.id and  l.source_article_id = p.id and l.target_x_coord_1920_1080 is not Null and l.target_y_coord_1920_1080 is not Null  and l.target_x_coord_1920_1080!=0 and l.target_y_coord_1920_1080!=0;')
            result = self._cursor.fetchall()
            for row in result:
                link = {}
                link['key']= row[0], row[1]
                link['x'] = row[2]
                link['y'] = row[3]
                link['out_degree'] = row[4]
                link['page_length'] = row[5]
                coords.append(link)
        except MySQLdb.Error, e:
            logging.error('error retrieving xy coord for all links links %s (%d)' % (e.args[1], e.args[0]))
        return coords

    def retrieve_all_links_coords_degree(self):

        coords = []
        try:
            self._cursor.execute('select l.source_article_id, l.target_article_id, l.target_x_coord_1920_1080, l.target_y_coord_1920_1080, f.degree, p.page_length_1920_1080 from links l, article_features f, page_length p where l.target_article_id=f.id and  l.source_article_id = p.id and l.target_x_coord_1920_1080 is not Null and l.target_y_coord_1920_1080 is not Null  and l.target_x_coord_1920_1080!=0 and l.target_y_coord_1920_1080!=0;')
            result = self._cursor.fetchall()
            for row in result:
                link = {}
                link['key']= row[0], row[1]
                link['x'] = row[2]
                link['y'] = row[3]
                link['degree'] = row[4]
                link['page_length'] = row[5]
                coords.append(link)
        except MySQLdb.Error, e:
            logging.error('error retrieving xy coord for all links links %s (%d)' % (e.args[1], e.args[0]))
        return coords

    def retrieve_all_links_coords_clustering(self):

        coords = []
        try:
            self._cursor.execute('select l.source_article_id, l.target_article_id, l.target_x_coord_1920_1080, l.target_y_coord_1920_1080, f.local_clustering, p.page_length_1920_1080 from links l, article_features f, page_length p where l.target_article_id=f.id and  l.source_article_id = p.id and l.target_x_coord_1920_1080 is not Null and l.target_y_coord_1920_1080 is not Null  and l.target_x_coord_1920_1080!=0 and l.target_y_coord_1920_1080!=0;')
            result = self._cursor.fetchall()
            for row in result:
                link = {}
                link['key']= row[0], row[1]
                link['x'] = row[2]
                link['y'] = row[3]
                link['local_clustering'] = row[4]
                link['page_length'] = row[5]
                coords.append(link)
        except MySQLdb.Error, e:
            logging.error('error retrieving xy coord for all links links %s (%d)' % (e.args[1], e.args[0]))
        return coords

    def retrieve_all_links_coords_kcore(self):

        coords = []
        try:
            self._cursor.execute('select l.source_article_id, l.target_article_id, l.target_x_coord_1920_1080, l.target_y_coord_1920_1080, f.kcore, p.page_length_1920_1080 from links l, article_features f, page_length p where l.target_article_id=f.id and  l.source_article_id = p.id and l.target_x_coord_1920_1080 is not Null and l.target_y_coord_1920_1080 is not Null  and l.target_x_coord_1920_1080!=0 and l.target_y_coord_1920_1080!=0;')
            result = self._cursor.fetchall()
            for row in result:
                link = {}
                link['key']= row[0], row[1]
                link['x'] = row[2]
                link['y'] = row[3]
                link['kcore'] = row[4]
                link['page_length'] = row[5]
                coords.append(link)
        except MySQLdb.Error, e:
            logging.error('error retrieving xy coord for all links links %s (%d)' % (e.args[1], e.args[0]))
        return coords

    def retrieve_all_links_coords_eigenvector(self):

        coords = []
        try:
            self._cursor.execute('select l.source_article_id, l.target_article_id, l.target_x_coord_1920_1080, l.target_y_coord_1920_1080, f.eigenvector_centr, p.page_length_1920_1080 from links l, article_features f, page_length p where l.target_article_id=f.id and  l.source_article_id = p.id and l.target_x_coord_1920_1080 is not Null and l.target_y_coord_1920_1080 is not Null  and l.target_x_coord_1920_1080!=0 and l.target_y_coord_1920_1080!=0;')
            result = self._cursor.fetchall()
            for row in result:
                link = {}
                link['key']= row[0], row[1]
                link['x'] = row[2]
                link['y'] = row[3]
                link['kcore'] = row[4]
                link['eigenvector_centr'] = row[5]
                coords.append(link)
        except MySQLdb.Error, e:
            logging.error('error retrieving xy coord for all links links %s (%d)' % (e.args[1], e.args[0]))
        return coords

    def retrieve_internalcounts_degree(self):
        coords = []
        try:
            self._cursor.execute('select a.in_degree, sum(c.counts) as counts from clickstream_derived c, article_features a where c.link_type_derived= %s  and a.id=c.curr_id  group by c.curr_id limit 500;', ("internal-link",))
            result = self._cursor.fetchall()
            for row in result:
                #link = {}
                #link['in_degree'] = row[0]
                #link['counts'] = row[1]
                coords.append(row[0], row[1])
        except MySQLdb.Error, e:
            logging.error('error retrieving xy coord for all links links %s (%d)' % (e.args[1], e.args[0]))
        return coords
