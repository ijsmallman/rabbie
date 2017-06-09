import pytest


def pytest_addoption(parser):
    parser.addoption("--online",
                     action="store_true",
                     help="run online tests")
    parser.addoption("--slow",
                     action="store_true",
                     help="run slow tests")
    parser.addoption("--hostname",
                     action="store",
                     default='localhost',
                     help="specify IP of levelsensor")



