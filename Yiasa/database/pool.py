from multiprocessing import Process, Queue, current_process
import multiprocessing
import database
import random
import time
import sqlite3
import datetime
import threading
import uuid

db = database.Database()
lock = threading.Lock()

class Pool():
    def __init__(self):
        self.database = database.Database()
        self.processes = []
        self.lock = threading.Lock()
    
    def start_process_queue(self, queue):
        print('start_process_queue')
        p = Process(target=process_queue, args=(queue,), name=uuid.uuid4().hex)
        print('start_process_queue2')
        self.processes.append(p)
        print('start_process_queue3')
        p.start()
        print('start_process_queue4')

def process_queue(queue):
    global db, lock
    for item in iter(queue.get, None):
        q = f'INSERT INTO test VALUES ({item})'
        lock.acquire()
        try:
            #print(multiprocessing.current_process().name)
            db.query(q)
        finally:
            lock.release()

def add_queue(queue, num1, num2):
    for i in range(num1, num2):
        queue.put(i)
    return queue

def main():
    pool = Pool()

    q1 = Queue()
    q1 = add_queue(q1, 1000, 2000)
    q2 = Queue()
    q2 = add_queue(q2, 2000, 3000)
    q3 = Queue()
    q3 = add_queue(q3, 2000, 3000)

    pool.start_process_queue(q1)
    pool.start_process_queue(q2)
    pool.start_process_queue(q3)
    while True:
        pool.database.cursor_query("SELECT MAX(i) FROM test")
        print(len(pool.processes))
        time.sleep(0.4)
        for proc in pool.processes:
            if proc.is_alive() is False:
                proc.join()
                pool.processes.remove(proc)
                print('stopped proc')
    

if __name__ == '__main__':
    main()