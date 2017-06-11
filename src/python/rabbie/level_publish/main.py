import argparse
import sys
import logging
from typing import List

from rabbie.database import DataBase
from .publish import Publisher
from .notify import Email
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
    notifier = Email(smtp_server=config['smtp_server'],
                     smtp_port=config['smtp_port'],
                     username=config['username'],
                     password=config['password'],
                     recipients=config['recipients'])

    entries = db.fetch_entries(filter_synced=True)
    logger.info('Found {} entries in {} to push to server'.format(len(entries),
                                                                  config['database']))

    for entry in entries:
        publisher.push_entry(entry)
        db.update_sync_status(entry['measured-at'], True)
        try:
            if entry['name'] == 'water-level' and entry['value'] >= config['notification_water_level']:
                notifier.notify('WARNING: High burn water level',
                                'Be aware, water level in the burn was measured at {} to be ' +
                                '{}mm high.'.format(entry['measured-at'], entry['value']))
        except Exception as e:
            logger.error('Cannot notify recipients: {}'.format(config['recipients']))
            raise IOError('Cannot notify recipients by email') from e

if __name__ == '__main__':
    main()
