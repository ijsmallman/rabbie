import json
from os.path import join, dirname
from .schema import validate_message


CONFIG_SCHEMA_FILENAME = 'config_schema.json'


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
