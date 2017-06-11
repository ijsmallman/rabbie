import datetime
from typing import Tuple
from os.path import dirname, join
import json
import logging
from urllib.request import urlopen


from rabbie.utils import load_schema, validate_message


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
        validate_message(join(dirname(dirname(dirname(dirname(__file__)))),
                              "schemas",
                              MEASUREMENT_SCHEMA_FILENAME),
                         msg)
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
