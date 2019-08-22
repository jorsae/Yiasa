import pytest
import sys
sys.path.append('database/')
import database
import os
import random

dbFile = 'tests/database/pytest.sql'
db = database.Database(db_file=dbFile)

@pytest.fixture(scope="module")
def create_table(request):
    db.query("DROP TABLE IF EXISTS test")
    db.query("CREATE TABLE test (i int)")
    
    def fin():
        db.connection.close()
        os.remove(dbFile)
    request.addfinalizer(fin)

def test_create_database():
    assert(os.path.isfile(dbFile)) == True

def test_query(create_table):
    assert(db.query("INSERT INTO test VALUES (1)")) == True

def test_query_fails(create_table):
    assert(db.query("INSERT INTI test VALU (1)")) == False

def test_query_get(create_table):
    number = random.randint(1, 1e5)
    db.query(f'INSERT INTO test VALUES ({number})')
    result = db.query_get(f'SELECT * FROM test where i = \'{number}\'')
    assert(result[0][0]) == number

def test_query_get_fails(create_table):
    number = random.randint(1, 1e5)
    db.query(f'INSERT INTO test VALU ({number})')
    result = db.query_get(f'SELECT * FROM test where i = \'{number}\'')
    assert(result) == []