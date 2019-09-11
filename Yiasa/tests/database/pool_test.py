import pytest
import sys
sys.path.append('database/')
import pool
from pq import PoolQuery

def test_pool_empty():
    queue = pool.Pool()
    assert(queue.empty()) == True

def test_pool_not_empty():
    queue = pool.Pool()
    queue.processing = True # disables processing of data
    queue.put(PoolQuery(1, 'test'))
    assert(queue.empty()) == False

def test_pool_get_while_empty():
    queue = pool.Pool()
    assert(queue.get()) == None

def test_pool_priority_queue():
    queue = pool.Pool()
    queue.processing = True # disables processing of data

    expected = PoolQuery('test3', priority=-1)
    queue.put(PoolQuery('test1'))
    queue.put(expected)
    queue.put(PoolQuery('test2'))

    assert(queue.get()) == expected