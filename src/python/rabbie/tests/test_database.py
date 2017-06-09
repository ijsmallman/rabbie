import pytest
from unittest.mock import patch
from os.path import join, dirname, exists
from datetime import datetime, timezone
import logging
import uuid
from rabbie.database import DataBase


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


slow = pytest.mark.skipif(
    not pytest.config.getoption("--slow"),
    reason="need --slow option to run"
)


def test_create_database(tmpdir):
    db_no_ext = tmpdir.join('{}'.format(uuid.uuid4()))
    db_with_ext = tmpdir.join('{}.db'.format(uuid.uuid4()))
    DataBase(db_no_ext.strpath)
    DataBase(db_with_ext.strpath)
    assert exists('{}.db'.format(db_no_ext))
    assert exists('{}'.format(db_with_ext))


def test_insert_vals_and_count_entries(tmpdir):
    db_path = tmpdir.join('{}'.format(uuid.uuid4()))
    db = DataBase(db_path.strpath)
    n = 10
    for i in range(n):
        db.insert_val('test', datetime.utcnow(), i)
    assert db.entry_count('test') == n
    assert db.entry_count('made_up_name') == 0


@pytest.fixture(scope='session')
def test_db(tmpdir_factory):
    db_path = tmpdir_factory.mktemp('db').join('test_db.db')
    db = DataBase(db_path.strpath)

    entries = [(datetime(2017, 1, 1, 0, 0, 0), 0),
               (datetime(2017, 3, 1, 0, 0, 0), 1),
               (datetime(2017, 6, 1, 0, 0, 0), 2)]
    for t, v in entries:
        db.insert_val('test', t, v)
    return db


def test_fetch_all_vals(test_db):
    vals = test_db.fetch_entries()
    assert len(vals) == 3


def test_fetch_from_date(test_db):
    vals = test_db.fetch_entries(from_datetime=datetime(2017, 1, 1, 12, 0, 0))
    assert len(vals) == 2
    fetched_times = [v['timestamp'] for v in vals]
    for t in [datetime(2017, 3, 1, 0, 0, 0),
              datetime(2017, 6, 1, 0, 0, 0)]:
        assert (t in fetched_times)
    assert ((datetime(2017, 1, 1, 0, 0, 0), 0) not in fetched_times)


def test_fetch_to_date(test_db):
    vals = test_db.fetch_entries(to_datetime=datetime(2017, 4, 1, 0, 0, 0))
    assert len(vals) == 2
    fetched_times = [v['timestamp'] for v in vals]
    for t in [datetime(2017, 1, 1, 0, 0, 0),
              datetime(2017, 3, 1, 0, 0, 0)]:
        assert (t in fetched_times)
    assert ((datetime(2017, 6, 1, 0, 0, 0), 0) not in fetched_times)


def test_fetch_between_dates(test_db):
    vals = test_db.fetch_entries(to_datetime=datetime(2017, 4, 1, 0, 0, 0),
                                 from_datetime=datetime(2017, 1, 1, 12, 0, 0))
    assert len(vals) == 1
    assert datetime(2017, 3, 1, 0, 0, 0) == vals[0]['timestamp']


def test_fetch_datetime(test_db):
    t = datetime(2017, 3, 1, 0, 0, 0)
    val = test_db.fetch_entry(t)
    assert val is not None
    assert val['timestamp'] == t


def test_update_status(test_db):
    t = datetime(2017, 3, 1, 0, 0, 0)
    test_db.update_sync_status(t, True)
    val = test_db.fetch_entry(t)
    assert val['is_synced']
    test_db.update_sync_status(t, False)
    val = test_db.fetch_entry(t)
    assert not val['is_synced']
