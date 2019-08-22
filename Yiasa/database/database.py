import sqlite3
import logging

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
    def __init__(self):
        self.connection = sqlite3.connect('test.sql', check_same_thread=False)
        self.query("DROP TABLE IF EXISTS test")
        self.query("CREATE TABLE test(i integer)")
        logging.info('Database created')
        self.connection.execute('pragma journal_mode=DELETE')
        #self.connection.execute('pragma journal_mode=WAL')

    def start_transaction(self):
        self.connection.execute('BEGIN')
    
    def end_transaction(self):
        self.connection.execute('END')
    
    def query(self, query):
        self.connection.execute(query)
        self.connection.commit()

    def cursor_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        for row in cursor:
            print(row)