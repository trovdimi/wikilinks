import MySQLdb
import logging
import time

MYSQL_DEAD_LOCK_ERROR = 1213

class MySQLBuildView:
    """The MySQLBuildView class allows database access optimized to
       build the disambiguation database
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

    def insert_article(self, id, rev_id, title):
        """saves an article in the database

           @param id the id of the article
           @param title the title of the article 
        """
        try:
            self._cursor.execute('INSERT INTO articles(id, rev_id, title) VALUES(%s, %s, %s);',
                (id, rev_id, title))
        except MySQLdb.Error, e:
            logging.error('error saving article "%s" to database: %s (%d)' 
                % (title.encode('ascii', 'ignore'), e.args[1], e.args[0]))


    def insert_redirect(self, source_name, target_name):
        """saves a redirect in the database

        @param source_name the name of the source article
        @param target_name the name of the target article
        """
        try:
            self._cursor.execute('INSERT INTO redirects(source_article_name, target_article_name) VALUES(%s, %s);',
                (source_name, target_name))
        except MySQLdb.Error, e:
            logging.error('error saving redirect "%s" --> "%s" to database: %s (%d)' 
                % (source_name.encode('ascii', 'ignore'), target_name.encode('ascii', 'ignore'), e.args[1], e.args[0]))


    def commit(self):
        '''commits the changes
        '''
        self._db_connection.commit()


    def reset_cache(self):
        """resets the internal cache and thus prevents it from growing too big
        """
        self._article_id_cache = {}

    def _resolve_title(self, title):
        """resolves an article and returns its id

           @param title the title of the article
        """
        title = title.strip()
        if title in self._article_id_cache:
            return self._article_id_cache[title]

        try:
            if len(title) > 0:
                t = title[0].upper() + title[1:]
            else:
                t = title
            self._cursor.execute('SELECT id FROM articles WHERE title=%s;', (t,))
            row = self._cursor.fetchone()
            if row == None:
                self._cursor.execute('SELECT id FROM articles WHERE title=(SELECT target_article_name FROM redirects WHERE source_article_name=%s);',
                        (title,))
                row = self._cursor.fetchone()

            if row == None:
                self._article_id_cache[title] = None
            else:
                self._article_id_cache[title] = row[0]
        except MySQLdb.Error, e:
            logging.error('error resolving article "%s": %s (%d)'
                % (title.encode('ascii', 'ignore'), e.args[1], e.args[0]))

        return self._article_id_cache[title]
