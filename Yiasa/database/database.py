import sqlite3

"""
Example below does not work.
https://stackoverflow.com/questions/393554/python-sqlite3-and-concurrency
https://docs.python.org/3/library/multiprocessing.html

Says switching to multiprocessing.

Lots of people say sqlite does not support multiple connections properly.

Best solution is probably to have a Pool.
    https://twistedmatrix.com/trac/

"""

class Database():
    def __init__(self):
        self.connection = sqlite3.connect('test.sql', check_same_thread=False)
        self.connection.isolation_level = None
        self.cursor = None

    def start_transaction(self):
        self.cursor = self.connection.cursor()
        self.cursor.execute('BEGIN')
    
    def end_transaction(self):
        self.cursor.execute('END')
    
    def query(self, query):
        self.cursor.execute(query)

    def cursor_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        for row in cursor:
            print(row)

throw = Database()
throw.start_transaction()
throw.query("DROP TABLE IF EXISTS test")
throw.query("CREATE TABLE test (i integer)")
throw.end_transaction()

db = Database()
db2 = Database()

db.start_transaction()
for _ in range(3):
    db.query(f'INSERT INTO test VALUES({_})')

db2.start_transaction()
for _ in range(2):
    db2.query(f'INSERT INTO test VALUES({_})')
db2.end_transaction()
db.end_transaction()

db.cursor_query("SELECT * from test")