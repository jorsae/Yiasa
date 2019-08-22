import threading
import queue
import random
import time
import database
from PoolQuery import PoolQuery

class Pool(queue.PriorityQueue):
    def __init__(self):
        queue.PriorityQueue.__init__(self)
        self.thread = None
        self.processing = False
        self.database = database.Database()
    
    def put(self, item):
        queue.PriorityQueue.put(self, item)
        self.start_process()
    
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
            print(f'Processing: {poolQuery}')
            self.database.query(poolQuery.query)
        self.processing = False
        print(f'queue empty: {queue.PriorityQueue.empty(self)}')
    
    def empty(self):
        return queue.PriorityQueue.empty(self)

def fill():
    for _ in range(random.randint(1, 4)):
        a.put(PoolQuery(1, 'a'))

a = Pool()
a.put(PoolQuery(-1, 'DROP TABLE IF EXISTS test'))
a.put(PoolQuery(-1, 'CREATE TABLE test (i integer)'))
a.put(PoolQuery(-1, 'INSERT INTO test VALUES(1)'))
a.put(PoolQuery(-1, 'INSERT INTO test VALUES(2)'))
a.put(PoolQuery(-1, 'INSERT INTO test VALUES(3)'))

time.sleep(2)

while True:
    a.database.cursor_query("SELECT COUNT(*) FROM test")
    if a.empty():
        time.sleep(random.random())
        a.put(PoolQuery(-1, 'INSERT INTO test VALUES(1)'))