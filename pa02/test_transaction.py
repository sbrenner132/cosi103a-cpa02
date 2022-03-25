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
    cat1 = {'item_num': 12, 'amount': 13, 'category': 'parking',
            'date': '06-06-2001', 'description': 'the parking ticket actually'}
    cat2 = {'item_num': 10, 'amount': 1, 'category': 'parking',
            'date': '05-05-2001', 'description': 'the parking ticket actually, why????'}

    id1 = empty_db.add(cat1)
    id2 = empty_db.add(cat2)

    yield empty_db

    empty_db.delete(id1)
    empty_db.delete(id2)


@pytest.mark.summarize_by_date
def test_summarize_by_date(small_db):
    expected = {'rowid': 1, 'item_num': 12, 'amount': 13, 'category': 'parking',
                'date': '06-06-2001', 'description': 'the parking ticket actually'}
    actual = small_db.summarize_by_date(
        '06-06-2001')[0]  # get the first item in the list
    assert len(expected) == len(actual)
    assert expected == actual


@pytest.mark.summarize_by_month
def test_summarize__by_month(small_db):
    expected = [{'rowid': 1, 'item_num': 12, 'amount': 13, 'category': 'parking',
                 'date': '06-06-2001', 'description': 'the parking ticket actually'}]
    actual = small_db.summarize_by_month('06')
    assert len(expected) == len(actual)
    assert len(expected[0]) == len(actual[0])
    assert expected[0] == actual[0]


@pytest.mark.summarize_by_year
def test_summarize_by_year(small_db):
    expected = [{'rowid': 1, 'item_num': 12, 'amount': 13, 'category': 'parking', 'date': '06-06-2001', 'description': 'the parking ticket actually'},
                {'rowid': 2, 'item_num': 10, 'amount': 1, 'category': 'parking', 'date': '05-05-2001', 'description': 'the parking ticket actually, why????'}]
    actual = small_db.summarize_by_year('2001')
    assert len(expected) == len(actual)
    assert len(expected[0]) == len(actual[0])
    assert len(expected[1]) == len(actual[1])
    assert expected[0] == actual[0]
    assert expected[1] == actual[1]


@pytest.mark.summarize_by_category
def test_summarize_by_category(small_db):
    expected = [{'rowid': 1, 'item_num': 12, 'amount': 13, 'category': 'parking', 'date': '06-06-2001', 'description': 'the parking ticket actually'},
                {'rowid': 2, 'item_num': 10, 'amount': 1, 'category': 'parking', 'date': '05-05-2001', 'description': 'the parking ticket actually, why????'}]
    actual = small_db.summarize_by_category('parking')
    assert len(expected) == len(actual)
    assert len(expected[0]) == len(actual[0])
    assert len(expected[1]) == len(actual[1])
    assert expected[0] == actual[0]
    assert expected[1] == actual[1]
