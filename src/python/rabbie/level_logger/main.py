import argparse
import sys
import logging
from typing import List

from rabbie.database import DataBase
from rabbie.level_logger.sensor import LevelSensor
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
    parser = argparse.ArgumentParser(description="Log sensor value to a database")
    parser.add_argument('config',
                        type=str,
                        help='path to config file')
    return parser.parse_args(cmd_args)


def main() -> None:
    """
    Main entry point to the application
    """
    init_root_logger('level_logger.log')

    parsed_args = parse_args(sys.argv[1:])

    config = load_config(parsed_args.config)

    db = DataBase(name=config["database"])
    lvl_sens = LevelSensor(hostname=config["hostname"])

    db.insert_val("water-level",
                  *lvl_sens.reading)


if __name__ == '__main__':
    main()
