from pkg_resources import parse_requirements
from setuptools import setup

import project

def load_requirements(filename: str) -> list:
    with open(filename, 'r', encoding="utf-8") as file:
        return [f"""{req.name}{f"[{','.join(req.extras)}]" if req.extras else ''}{req.specifier}"""
                for req in parse_requirements(file.read())]


setup(
    name=project.NAME,
    version=project.VERSION,
    packages=project.MODULES,
    url=project.URL,
    license=project.LICENSE,
    author=project.AUTHOR,
    author_email=project.EMAIL,
    description=project.DESCRIPTION,
    install_requires=load_requirements('requirements.txt'),
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'mammon-api = mammon_api.__main__',
        ]
    },
)
