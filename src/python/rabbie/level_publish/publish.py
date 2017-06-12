from urllib import request, parse
import logging
import json


logger = logging.getLogger(__name__)


class Publisher:

    def __init__(self, url: str, api_token: str) -> None:
        self.url = url
        self.api_token = api_token

    def push_entry(self, entry: dict) -> None:
        """
        Push database entry to url

        Parameters
        ----------
        entry: dict
            database entry to push

        Raises
        ------
        IOError
            if request fails
        """
        logger.info("Pushing entry '{}' to '{}'".format(entry, self.url))
        data = json.dumps(entry, default=str).encode('utf-8')
        req = request.Request(self.url,
                              data=data,
                              headers={'content-type': 'application/json',
                                       'user-agent': 'Mozilla/5.0',
                                       'api-token': '{}'.format(self.api_token)})
        try:
            request.urlopen(req)
        except Exception as e:
            logger.error(e)
            raise IOError("Cannot push entry '{}' to {}".format(data, self.url)) from e


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    import datetime
    if isinstance(obj, datetime.datetime):
        serial = obj.isoformat()
        return serial
    raise TypeError ("Type %s not serializable" % type(obj))