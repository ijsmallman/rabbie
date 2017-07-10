import json
from os.path import join, dirname
from typing import List
import argparse
from .schema import validate_message


CONFIG_SCHEMA_FILENAME = 'config_schema.json'


def parse_cmd_args(cmd_args: List[str]) -> argparse.Namespace:
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
    parser = argparse.ArgumentParser()
    parser.add_argument('config',
                        type=str,
                        help='path to config file')
    return parser.parse_args(cmd_args)


def load_config(config_path: str)->dict:
    """
    Load config json file

    Parameters
    ----------
    config_path: str
        path to config file conforming to config_schema.json

    Returns
    -------
    config: dict
    """
    with open(config_path, 'r') as f:
        config = json.load(f)
    schema_path = join(dirname(dirname(dirname(dirname(__file__)))),
                       'schemas',
                       CONFIG_SCHEMA_FILENAME)
    validate_message(schema_path, config)
    return config
