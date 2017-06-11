import pytest
from datetime import datetime
import random
from os.path import dirname, join, exists

from rabbie.database import DataBase
from rabbie.level_publish.publish import Publisher
from rabbie.utils import load_config


@pytest.fixture(scope='session')
def test_db(tmpdir_factory):
    db_path = tmpdir_factory.mktemp('db').join('test_db.db')
    db = DataBase(db_path.strpath)

    for i in range(10):
        db.insert_val('test-val', datetime.utcnow(), random.randint(0, 4999))

    return db


@pytest.fixture(scope='session')
def publisher():
    config_path = join(dirname(dirname(dirname(dirname(dirname(__file__))))), 'config.json')
    assert exists(config_path)
    config = load_config(config_path)
    p = Publisher(config['server_url'], config['api_token'])
    return p


def test_push(publisher, test_db):
    entries = test_db.fetch_entries()
    for entry in entries:
        publisher.push_entry(entry)
