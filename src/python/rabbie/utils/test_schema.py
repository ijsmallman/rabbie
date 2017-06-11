import pytest
from os.path import dirname, join
from rabbie.utils import load_schema, validate_message


from rabbie.level_logger.sensor import MEASUREMENT_SCHEMA_FILENAME

@pytest.fixture(scope='module')
def schema_path():
    return join(dirname(dirname(dirname(dirname(__file__)))),
                "schemas",
                MEASUREMENT_SCHEMA_FILENAME)


def test_import_schema_error():
    with pytest.raises(IOError):
        load_schema('made_up_path.json')


def test_import_valid_schema(schema_path):
    schema = load_schema(schema_path)
    assert isinstance(schema, dict)


@pytest.fixture(scope='module')
def valid_reading():
    return {
      "distance": {
        "value": 5000,
        "units": "mm"
      },
      "last_update": {
        "value": 60,
        "units": "s"
      }
    }


def test_validation_error(schema_path):
    invalid_msg = {}
    with pytest.raises(IOError):
        validate_message(schema_path, invalid_msg)


def test_validation(schema_path, valid_reading):
    validate_message(schema_path, valid_reading)
