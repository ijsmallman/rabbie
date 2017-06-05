import datetime
from typing import Tuple
from os.path import dirname, join
import json
import jsonschema
import logging
from urllib.request import urlopen


MEASUREMENT_SCHEMA_FILENAME = "sensor_reading_schema.json"


logger = logging.getLogger(__name__)


class LevelSensor:

    def __init__(self, hostname: str) -> None:
        """
        Initialise LevelSensor model

        Parameters
        ----------
        hostname: str
            network name for level sensor
        """
        self._hostname = hostname

    @staticmethod
    def load_schema(schema_path: str) -> dict:
        """
        Load json schema for measurement messages

        Parameters
        ----------
        schema_path: str
            path to the message schema json file

        Returns
        -------
        schema: dict
            the schema

        Raises
        ------
        IOError
            if cannot load json schema
        """
        try:
            with open(schema_path, "r") as fs:
                schema = json.load(fs)
        except Exception as e:
            logger.error("Cannot load message schema '{}': {}".format(schema_path, e))
            raise IOError from e
        return schema

    @staticmethod
    def validate_message(msg: dict) -> None:
        """
        Validate received message against sensor reading schema

        Parameters
        ----------
        msg: dict
            sensor reading to validate

        Raises
        ------
        IOError
            if message doesn't validate
        """
        schema_path = join(dirname(dirname(dirname(dirname(__file__)))),
                           "schemas",
                           MEASUREMENT_SCHEMA_FILENAME)
        schema = LevelSensor.load_schema(schema_path)
        try:
            jsonschema.validate(msg, schema)
        except jsonschema.ValidationError as e:
            logger.error("Message '{}' does not validate against schema: {}".format(msg, e))
            raise IOError from e

    def http_request(self) -> dict:
        """
        Request current water level measurement from sensor

        Returns
        -------
        msg: dict
            reading from

        Raises
        ------
        IOError
            if GET request fails
        """
        url = 'http://{}'.format(self._hostname)
        try:
            with urlopen(url) as response:
                msg = response.read()
        except Exception as e:
            logger.error('Request for current level from {} failed: {}'.format(url, e))
            raise IOError from e
        msg = json.loads(msg)
        LevelSensor.validate_message(msg)
        return msg

    @staticmethod
    def timestamp(msg: dict) -> datetime.datetime:
        """
        Get UTC time for given sensor reading
        
        Parameters
        ----------
        msg: dict
            Sensor reading

        Returns
        -------
        timestamp: datetime.datetime
            Reading UTC
        """
        sys_time = current_system_time()
        time_since_last_update = msg['last_update']['value']
        return sys_time - datetime.timedelta(seconds=time_since_last_update)

    @property
    def reading(self) -> Tuple[datetime.datetime, int]:
        """
        Current water level

        Returns
        -------
        timestamp: datetime.datetime
            UTC when measurement was taken (within a few seconds)
        val: int
            current water level (mm)
        """
        msg = self.http_request()
        t = LevelSensor.timestamp(msg)
        v = msg['distance']['value']
        return t, v


def current_system_time() -> datetime.datetime:
    """
    Get current UTC

    Returns
    -------
    timestamp: datetime.datetime
    """
    return datetime.datetime.utcnow()
