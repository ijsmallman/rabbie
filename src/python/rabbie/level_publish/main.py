import argparse
import sys
import logging
from typing import List

from rabbie.database import DataBase
from rabbie.level_publish import Publisher
from rabbie.utils import init_root_logger, load_config

logger = logging.getLogger(__name__)


def parse_args(cmd_args: List[str]) -> argparse.Namespace:
    """
    Parse command line arguments

    Parameters
    ----------
    cmd_args: List[str]
        list of argument strings taken from command line to be parsed

    Returns
    -------
    parsed_args: argparse.Namespace
        arguments assigned as attributes of the Namespace object
    """
    parser = argparse.ArgumentParser(description="Push level sensor values in database to 'the cloud'")
    parser.add_argument('config',
                        type=str,
                        help='path to config file')
    return parser.parse_args(cmd_args)


def main() -> None:
    """
    Main entry point to the application
    """
    init_root_logger('level_publish.log')

    parsed_args = parse_args(sys.argv[1:])

    config = load_config(parsed_args.config)

    db = DataBase(name=config["database"])
    publisher = Publisher(url=config['server_url'],
                          api_token=config['api_token'])

    entries = db.fetch_entries(filter_synced=True)
    logger.info('Found {} entries in {} to push to server'.format(len(entries),
                                                                  config['database']))

    for entry in entries:
        publisher.push_entry(entry)
        db.update_sync_status(entry['measured-at'], True)

if __name__ == '__main__':
    main()
