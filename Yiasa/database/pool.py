import threading
import queue
import random
import time
import database
from pq import PoolQuery

class Pool(queue.PriorityQueue):
    def __init__(self):
        queue.PriorityQueue.__init__(self)
        self.thread = None
        self.processing = False
        self.database = database.Database()
        print('init db')
    
    def put(self, item):
        queue.PriorityQueue.put(self, item)
        self.start_process()
    
    def get(self):
        if self.empty():
            return None
        return queue.PriorityQueue.get(self)

    def start_process(self):
        if queue.PriorityQueue.empty(self):
            self.thread.join()
            self.thread = None
        else:
            if self.processing is False:
                self.start_thread()

    def start_thread(self):
        self.thread = threading.Thread(target=self.process)
        self.thread.start()

    def process(self):
        self.processing = True
        while not queue.PriorityQueue.empty(self):
            poolQuery = queue.PriorityQueue.get(self)
            #print(f'Processing: {poolQuery}')
            self.database.query(poolQuery.query)
        self.processing = False
        print(f'queue empty: {queue.PriorityQueue.empty(self)}')
    
    def empty(self):
        return queue.PriorityQueue.empty(self)

def fill():
    for _ in range(random.randint(1, 4)):
        a.put(PoolQuery(1, 'a'))

"""
a.put(PoolQuery(-1, 'DROP TABLE IF EXISTS test'))
a.put(PoolQuery(-1, 'CREATE TABLE test (i integer)'))
a.put(PoolQuery(100, 'INSERT INTO test VALUES(1)'))
a.put(PoolQuery(100, 'INSERT INTO test VALUES(2)'))
a.put(PoolQuery(100, 'INSERT INTO test VALUES(3)'))

time.sleep(2)

def fill():
    for _ in range(400):
        a.put(PoolQuery(100, 'INSERT INTO test VALUES(1)'))

iterations = 0
while True:
    a.database.cursor_query("SELECT COUNT(*) FROM test")
    time.sleep(1)
    if a.empty():
        iterations += 1
        fill()

a.database.cursor_query("SELECT COUNT(*) FROM test")
"""