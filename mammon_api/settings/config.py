"""Module configuration"""
import logging

from os import environ

DEBUG = bool(int(environ.get('DEBUG') or False))
LOG_LEVEL = logging.getLevelName((environ.get('LOG_LEVEL') or 'info' if not DEBUG else 'debug').upper())

SQLITE_ENGINE = f"sqlite:////data/mammon.sqlite3"

logging.basicConfig(level=LOG_LEVEL,
                    format="[%(asctime)s] %(levelname)s [%(funcName)s] %(message)s",
                    datefmt="%d/%b/%Y %H:%M:%S")
