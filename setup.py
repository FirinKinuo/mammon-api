from pkg_resources import parse_requirements
from setuptools import setup

NAME = 'mammon_api'
DESCRIPTION = 'API module of the Mammon Unit for receiving data from local database to Mammon Gateway via REST'
MODULES = ['mammon_api', 'mammon_api.settings', 'mammon_api.db', 'mammon_api.db.utils']

with open(file='VERSION', mode='r', encoding="UTF-8") as version_file:
    VERSION = version_file.read().replace("v", "")


def load_requirements(filename: str) -> list:
    with open(filename, 'r', encoding="utf-8") as file:
        return [f"""{req.name}{f"[{','.join(req.extras)}]" if req.extras else ''}{req.specifier}"""
                for req in parse_requirements(file.read())]


setup(
    name=NAME,
    version=VERSION,
    packages=MODULES,
    url='https://git.fkinuo.ru/mammon-api',
    license='AGPL-3.0',
    author='Firin Kinuo',
    author_email='deals@fkinuo.ru',
    description=DESCRIPTION,
    install_requires=load_requirements('requirements.txt'),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'mammon-api = mammon_api.__main__',
        ]
    },
)
