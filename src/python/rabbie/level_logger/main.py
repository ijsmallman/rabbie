import sys
import logging

from rabbie.database import DataBase
from rabbie.level_logger.sensor import LevelSensor
from rabbie.utils import init_root_logger, load_config, parse_cmd_args

logger = logging.getLogger(__name__)


def main() -> None:
    """
    Main entry point to the application
    """
    init_root_logger('level_logger.log')

    parsed_args = parse_cmd_args(sys.argv[1:])

    config = load_config(parsed_args.config)

    db = DataBase(name=config["database"])
    lvl_sens = LevelSensor(hostname=config["hostname"])

    db.insert_val("water-level",
                  *lvl_sens.reading)


if __name__ == '__main__':
    main()
