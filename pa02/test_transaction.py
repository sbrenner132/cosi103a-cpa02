'''
test_transaction runs unit and integration tests on the transaction module
'''

import pytest
from transaction import Transaction, to_trans_dict


@pytest.fixture
def dbfile(tmpdir):
    ''' create a database file in a temporary file system '''
    return tmpdir.join('test_tracker1.db')

@pytest.fixture
def empty_db(dbfile):
    ''' create an empty database '''
    db = Transaction(dbfile)
    yield db

@pytest.fixture
def small_db(empty_db):
    cat1 = {'row_id':1,'item_num':12, 'amount': 13, 'category': 'parking', 'date':'06-06-2001', 'description': 'the parking ticket actually'}
    print(cat1)

    id1=empty_db.add(cat1)

    yield empty_db

    empty_db.delete(id1)

@pytest.mark.summarize_by_date
def test_summarize_by_date(small_db):
    small_db.summarize_by_date('06-06-2111')

@pytest.mark.summarize_by_month
def test_summarize__by_month(small_db):
    small_db.summarize_by_month('06')

@pytest.mark.summarize_by_year
def test_summarize_by_year(small_db):
    small_db.summarize_by_year('2111')

@pytest.mark.summarize_by_category
def test_summarize_by_category(small_db):
    small_db.summarize_by_category('parking')
