from pkg_resources import resource_filename
from pathlib import Path

__all__ = [
    'AUTHOR',
    'EMAIL',
    'NAME',
    'LICENSE',
    'URL',
    'DESCRIPTION',
    'VERSION'
]

MODULES = ['mammon_api', 'mammon_api.settings', 'mammon_api.db', 'mammon_api.db.utils']

AUTHOR = 'Firin Kinuo'
EMAIL = 'deals@fkinuo.ru'
TELEGRAM = "https://t.me/fkinuo"
NAME = 'mammon_api'
LICENSE = 'AGPL-3.0'
URL = 'https://git.fkinuo.ru/mammon-api'
DESCRIPTION = 'API module of the Mammon Unit for receiving data from local database to Mammon Gateway via REST'
ROOT = Path(resource_filename(NAME, '')).parent

with open(file=Path(ROOT, 'VERSION'), mode='r', encoding="UTF-8") as version_file:
    VERSION = version_file.read().replace("v", "")
