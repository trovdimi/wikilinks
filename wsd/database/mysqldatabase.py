import MySQLdb as mysqldb
import logging
import time
from mysqlbuildview import MySQLBuildView
from mysqlworkview import MySQLWorkView

class MySQLDatabase:
    """The MySQLDatabase class allows to build and manage the
       access to a mysql database
    """

    def __init__(self, host='localhost', user='wikiwsd', passwd='wikiwsd', database='wikiwsd3'):
        """constructor

           @param host the host to connect to
           @param user the database user
           @param passwd the password to be used in the connection
           @param database the database to select on the server
        """
        self._host = host
        self._user = user
        self._passwd = passwd
        self._database = database

    def build(self):
        """creates up the basic database structure
        """
        logging.info('Building database structure. Opening database connection...')
        connection = self._create_connection()
        cursor = connection.cursor()
        letters = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'other')
        start = time.clock()

        # build articles table
        logging.info('Building table articles...')
        cursor.execute('CREATE TABLE `articles` ('
                           '`id` BIGINT UNSIGNED NOT NULL PRIMARY KEY,'
                           '`rev_id` BIGINT UNSIGNED NOT NULL,'
                           '`title` VARCHAR(2000) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,'
                           'CONSTRAINT UNIQUE INDEX USING HASH(`title`),'
                           'CONSTRAINT UNIQUE INDEX USING HASH(`rev_id`)'
                       ') ENGINE=InnoDB;')

        # build redirects table
        logging.info('Building table redirects...')
        cursor.execute('CREATE TABLE `redirects` ('
                           '`id` BIGINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,'
                           '`source_article_name` VARCHAR(2000) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,'
                           '`target_article_name` VARCHAR(2000) CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,'
                           'CONSTRAINT UNIQUE INDEX USING HASH(`source_article_name`)'
                       ') ENGINE = InnoDB;')



        logging.info('closing database connection...')
        connection.close()

        end = time.clock()
        logging.info('DONE building tables (took %f seconds)' % (end-start))

    

    def get_build_view(self):
        """returns a new database view optimized for the build process
        """
        connection = self._create_connection()
        view = MySQLBuildView(connection)
        return view

    def get_work_view(self):
        """returns a new database view optimized for the disambiguation process
        """
        connection = self._create_connection()
        view = MySQLWorkView(connection)
        return view

    def _create_connection(self):
        con = mysqldb.connect(self._host, self._user, self._passwd, self._database, charset='utf8', use_unicode=True)
        return con
