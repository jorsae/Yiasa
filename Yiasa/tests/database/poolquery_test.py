import pytest
import sys
sys.path.append('database/')
import pq

def test_poolquery_str():
    poolQuery = pq.PoolQuery(1, 'testquery')
    assert(str(poolQuery)) == '1: testquery'

def test_poolquery_values():
    poolQuery = pq.PoolQuery(1, 'testquery')
    assert(poolQuery.priority) == 1
    assert(poolQuery.query) == 'testquery'

def test_poolquery_lt():
    poolQuery1 = pq.PoolQuery(1, 'testquery')
    poolQuery2 = pq.PoolQuery(2, 'testquery')
    assert(poolQuery1) < poolQuery2