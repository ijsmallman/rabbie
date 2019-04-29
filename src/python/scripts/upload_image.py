import logging
from rabbie import Credentials, CredentialsError, GoogleApiSession, GoogleApiSessionError

logger = logging.getLogger(__name__)


def main() -> int:
    """
    Upload an image to Google Photos
    """
    try:
        credentials = Credentials.from_secrets('photos_api_credentials.json')
    except CredentialsError:
        return 1

    try:
        session = GoogleApiSession(credentials)
    except GoogleApiSessionError:
        return 1

    return 0


if __name__ == '__main__':

    import sys
    import argparse
    from os import makedirs
    from os.path import join, dirname, exists

    parser = argparse.ArgumentParser('Upload an image to Google Photos')
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()

    if args.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    log_dir = join(
        dirname(dirname(dirname(dirname(__file__)))),
        'logs'
    )
    if not exists(log_dir):
        makedirs(log_dir)

    logging.basicConfig(
        level=log_level,
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%Y-%m-%dT%H:%M:%S',
        filename=join(log_dir, 'upload_image.log')
    )

    status_code = main()

    sys.exit(status_code)
