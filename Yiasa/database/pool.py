from multiprocessing import Process
import random
import time
import sqlite3

connection = sqlite3.connect('test.sql')

def query(query, sleep=True):
    connection.execute(query)
    connection.commit()
    if sleep:
        time.sleep(random.random())

def cursor_query():
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM test")
    print(cursor.fetchone())

def main():
    query("DROP TABLE IF EXISTS test", sleep=False)
    query("CREATE TABLE test (i integer)", sleep=False)

    #db = database.Database()
    procs = []
    while True:
        q = f'INSERT INTO test VALUES ({random.randint(1, 1e4)})'
        p1 = Process(target=query, args=(q, ))
        procs.append(p1)
        p1.start()
        time.sleep(random.random()* 2)
        for proc in procs:
            if proc.is_alive() is False:
                proc.join()
                procs.remove(proc)
        print(f'{cursor_query()} | {len(procs)}')

if __name__ == '__main__':
    main()