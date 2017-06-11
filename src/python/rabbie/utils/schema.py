import json
import jsonschema
import logging


logger = logging.getLogger(__name__)


def load_schema(schema_path: str) -> dict:
    """
    Load json schema for measurement messages

    Parameters
    ----------
    schema_path: str
        path to the message schema json file

    Returns
    -------
    schema: dict
        the schema

    Raises
    ------
    IOError
        if cannot load json schema
    """
    try:
        with open(schema_path, "r") as fs:
            schema = json.load(fs)
    except Exception as e:
        logger.error("Cannot load message schema '{}': {}".format(schema_path, e))
        raise IOError from e
    return schema


def validate_message(schema_path: str,
                     msg: dict) -> None:
    """
    Validate received message against sensor reading schema

    Parameters
    ----------
    schema_path: str
        path to schema file
    msg: dict
        sensor reading to validate

    Raises
    ------
    IOError
        if message doesn't validate
    """
    schema = load_schema(schema_path)
    try:
        jsonschema.validate(msg, schema)
    except jsonschema.ValidationError as e:
        logger.error("Message '{}' does not validate against schema: {}".format(msg, e))
        raise IOError from e
