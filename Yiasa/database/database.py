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

    def query(self, query, param=None):
        logging.info(f'{query} | {param}')
        try:
            if param is None:
                self.connection.execute(query)
            else:
                self.connection.execute(query, param)
            self.connection.commit()
            return True
        except Exception as e:
            logging.error(f'query(): {e}')
            return False

    def query_get(self, query, param=None):
        logging.info(f'{query} | {param}')
        # TODO: Add exception handling
        cursor = self.connection.cursor()
        if param is None:
            cursor.execute(query)
        else:
            cursor.execute(query, param)
        return cursor.fetchall()
    
    def query_exists(self, query, param=None):
        logging.info(f'{query} | {param}')
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, param)
            if cursor.fetchone() is None:
                return False
            else:
                return True
        except Exception as e:
            logging.error(f'query_exists(): {e}')
            return None

    def setup_database(self):
        if self.setup_table(query.create_table_domain(), (query.TABLE_DOMAIN, )) is not True:
            return False
        if self.setup_table(query.create_table_crawl_history(), (query.TABLE_CRAWL_HISTORY, )) is not True:
            return False
        if self.setup_table(query.create_table_crawl_queue(), (query.TABLE_CRAWL_QUEUE, )) is not True:
            return False
        if self.setup_table(query.create_table_emails(), (query.TABLE_EMAILS, )) is not True:
            return False
        
        logging.info('Database was set up correctly')
        return True
    
    def setup_table(self, create_query, table_name):
        table_exists = self.query_exists(query.table_exists(), table_name)
        if table_exists:
            return True
        elif table_exists is False:
            return self.query(create_query)
        else:
            logging.critical(f"setup database failed at '{table_name}'")
            return None