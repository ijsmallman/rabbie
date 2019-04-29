import json
import logging
from os.path import dirname, join

logger = logging.getLogger(__name__)


class CredentialsError(Exception):
    pass


class Credentials:

    def __init__(self, client_id: str, client_secret: str, project_id: str) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.project_id = project_id

    @classmethod
    def from_secrets(cls, filename: str) -> 'Credentials':
        credentials_path = join(
            dirname(dirname(dirname(dirname(__file__)))),
            'secrets',
            filename
        )

        logger.debug(
            'Loading credentials from %s',
            credentials_path
        )

        try:
            with open(credentials_path, 'r') as f:
                credentials = json.load(f)
        except IOError as e:
            logger.error("Failed to read credentials from %s", credentials_path)
            raise CredentialsError from e

        installed = credentials['installed']

        return Credentials(
            installed['client_id'],
            installed['client_secret'],
            installed['project_id']
        )
