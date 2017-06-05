import argparse
import sys
import logging
from typing import List

from rabbie.database import DataBase
from rabbie.level_logger.sensor import LevelSensor


logger = logging.getLogger(__name__)


def init_root_logger(file_log_level=logging.DEBUG,
                     console_log_level=logging.INFO) -> None:
    """
    Initialise logger and attach console and file handlers
    
    Parameters
    ----------
    file_log_level: [logging.NOTSET, logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
        log level for file log handler (default: logging.DEBUG)
    console_log_level: [logging.NOTSET, logging.DEBUG, logging.INFO, logging.WARNING, logging.ERROR, logging.CRITICAL]
        log level for console log handler (default: logging.INFO)
    """
    logging.getLogger().setLevel(logging.DEBUG)
    fh = logging.FileHandler('level_logger.log')
    fh.setLevel(file_log_level)
    ch = logging.StreamHandler()
    ch.setLevel(console_log_level)
    log_formatter = logging.Formatter('%(asctime)s %(name)s [%(levelname)s] %(message)s')
    fh.setFormatter(log_formatter)
    ch.setFormatter(log_formatter)
    logging.getLogger().addHandler(fh)
    logging.getLogger().addHandler(ch)


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
    parser = argparse.ArgumentParser(description="Log sensor value to a database")
    parser.add_argument('host',
                        type=str,
                        help='hostname of level sensor')
    parser.add_argument('db',
                        type=str,
                        help='database to log values to')
    return parser.parse_args(cmd_args)


def main() -> None:
    """
    Main entry point to the application
    """
    init_root_logger()

    parsed_args = parse_args(sys.argv[1:])

    db = DataBase(name=parsed_args.db)
    lvl_sens = LevelSensor(hostname=parse_args.host)

    db.insert_val("water-level",
                  *lvl_sens.reading)


if __name__ == '__main__':
    main()
