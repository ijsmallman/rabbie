import logging
import platform
from rabbie import google_auth, GoogleAuthError
from rabbie import DriveService, DriveServiceError
logger = logging.getLogger(__name__)


def upload(image_path: str) -> int:
    """
    Upload an image to Google Drive under folder named with computer hostname

    Parameters
    ----------
    image_path: str
        Path to image to upload

    Returns
    -------
    status_code: int
        Standard error code
    """

    try:
        credentials = google_auth()
    except GoogleAuthError:
        return 1

    hostname = platform.node()

    try:
        service = DriveService(credentials)
        service.upload_image(image_path, hostname)
    except DriveServiceError as e:
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
    parser.add_argument('image', type=str, help='Path to image file')
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

    status_code = upload(args.image)

    sys.exit(status_code)
