import pytest
import sys
sys.path.append('database/')
import pq

def test_poolquery_str():
    poolQuery = pq.PoolQuery('testquery')
    assert(str(poolQuery)) == f'{poolQuery.priority}: {poolQuery.query}'

def test_poolquery_priority_default_value():
    poolQuery = pq.PoolQuery('testquery')
    assert(poolQuery.priority) == 100

def test_poolquery_query_values():
    poolQuery = pq.PoolQuery('testquery')
    assert(poolQuery.query) == 'testquery'

def test_poolquery_lt():
    poolQuery1 = pq.PoolQuery('testquery', priority=100)
    poolQuery2 = pq.PoolQuery('testquery', priority=1)
    assert(poolQuery1) > poolQuery2