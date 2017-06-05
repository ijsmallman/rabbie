import pytest
from unittest.mock import patch
from os.path import join, dirname, exists
import datetime
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
    db1 = DataBase(db_no_ext.strpath)
    db2 = DataBase(db_with_ext.strpath)
    assert exists('{}.db'.format(db_no_ext))
    assert exists('{}'.format(db_with_ext))
