import logging
from rabbie import google_auth, GoogleAuthError
from rabbie import DriveService
logger = logging.getLogger(__name__)

def main() -> int:
    """
    Upload an image to Google Drive
    """

    try:
        credentials = google_auth()
    except GoogleAuthError:
        return 1

    try:
        service = DriveService(credentials)
        service.list_files()
    except Exception as e:
        logger.error(e)
        return 1

    return 0


if __name__ == '__main__':

    import sys
    import argparse
    from os import makedirs
    from os.path import join, dirname, exists

    parser = argparse.ArgumentParser('Upload an image to Google Drive')
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
