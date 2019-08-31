import sqlite3
import logging
import query

"""
Example below does not work.
https://stackoverflow.com/questions/393554/python-sqlite3-and-concurrency
https://docs.python.org/3/library/multiprocessing.html

Says switching to multiprocessing.

Lots of people say sqlite does not support multiple connections properly.

Best solution is probably to have a Pool.
    https://twistedmatrix.com/trac/

Read more regarding journal_mode here:
    https://www.sqlite.org/pragma.html#pragma_journal_mode
"""

class Database():
    def __init__(self, db_file='test.sql'):
        self.connection = sqlite3.connect(db_file, check_same_thread=False)
        self.connection.execute('pragma journal_mode=DELETE')
        #self.connection.execute('pragma journal_mode=WAL')

    def query(self, query):
        try:
            self.connection.execute(query)
            self.connection.commit()
            return True
        except:
            # TODO: Logging
            return False

    def query_get(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        return cursor.fetchall()
    
    def setup_database(self):
        self.query(query.create_table_fld())
        self.query(query.create_table_crawl_history())
        self.query(query.create_table_crawl_queue())
        self.query(query.create_table_emails())
        print('finished setup_database')
        a = self.query("INSERT INTO FLD VALUES ('http', 1, 2019-02-01)")
        print(a)