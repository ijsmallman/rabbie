from os.path import join, dirname, exists

from rabbie.utils import load_config


def test_load_config():
    config_path = join(dirname(dirname(dirname(dirname(dirname(__file__))))),
                       'config.json')
    assert exists(config_path)
    load_config(config_path)
