"""Module configuration"""
import sys
import logging

from os import environ
from pathlib import Path

IS_TEST = any(map(lambda path: 'tests' in path, sys.path))  # If test paths are found, then go to test mode

DEBUG = bool(int(environ.get('DEBUG'))) or False
LOG_LEVEL = logging.getLevelName((environ.get('LOG_LEVEL') if not DEBUG else 'debug').upper())

API_HOST = environ.get('API_HOST')
API_PORT = int(environ.get('API_PORT'))

SQLITE_ENGINE = f"sqlite:///{Path('/data', 'mammon.sqlite3')}"

logging.basicConfig(level=LOG_LEVEL,
                    format="[%(asctime)s] %(levelname)s [%(funcName)s] %(message)s",
                    datefmt="%d/%b/%Y %H:%M:%S")
