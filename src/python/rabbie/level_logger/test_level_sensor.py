import pytest
from unittest.mock import patch
import datetime
from rabbie.level_logger.sensor import LevelSensor
import logging


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

online = pytest.mark.skipif(
    not pytest.config.getoption("--online"),
    reason="need --online option to run"
)

slow = pytest.mark.skipif(
    not pytest.config.getoption("--slow"),
    reason="need --slow option to run"
)


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


def mocked_get_utc_now():
    dt = datetime.datetime(2017, 1, 1, 0, 1, 0)
    return dt


def mocked_http_request():
    return valid_reading()


@pytest.fixture(scope='module')
def fake_level_sensor():
    return LevelSensor('fake-sensor')


@patch('rabbie.level_logger.sensor.current_system_time', side_effect=mocked_get_utc_now)
def test_time_stamp(_, valid_reading):
    timestamp = LevelSensor.timestamp(valid_reading)
    assert timestamp == datetime.datetime(2017, 1, 1, 0, 0, 0)


@patch('rabbie.level_logger.sensor.LevelSensor.http_request', side_effect=mocked_http_request)
@patch('rabbie.level_logger.sensor.current_system_time', side_effect=mocked_get_utc_now)
def test_mock_reading(mock_request, mock_time):
    sensor = LevelSensor('fake_device')
    t, v = sensor.reading
    assert t == datetime.datetime(2017, 1, 1, 0, 0, 0)
    assert v == 5000


@slow
def test_http_request_error(fake_level_sensor):
    with pytest.raises(IOError):
        fake_level_sensor.reading


@online
def test_hello_world(request):
    hostname = pytest.config.getoption('--hostname')
    sensor = LevelSensor(hostname)
    t, v = sensor.reading
    logger.info('Sensor reading: ({}, {})'.format(t, v))
