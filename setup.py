import re

from setuptools import find_packages, setup

try:
    from pathlib import Path
except:
    from pathlib2 import Path


def read(filename):
    file_path = Path(__file__).parent / filename
    text_type = type(u"")
    with open(file_path, mode="r", encoding='utf-8') as f:
        return re.sub(text_type(r':[a-z]+:`~?(.*?)`'), text_type(r'``\1``'), f.read())


def get_requires():
    r_path = Path(__file__).parent / 'requirements.txt'
    if r_path.exists():
        with open(r_path) as f:
            required = f.read().splitlines()
    else:
        requred = []
    return required


setup(
    name="csv_zip_rsync",
    version="0.1.3",
    url="https://github.com/fx-kirin/csv_zip_rsync",
    license='MIT',
    scripts=["bin/csv_zip_rsync", "csv2zip"],

    author="fx-kirin",
    author_email="fx.kirin@gmail.com",

    description="compress csv to zip and rsync to remote server",
    long_description=read("README.rst"),

    packages=find_packages(exclude=('tests',)),

    install_requires=get_requires(),

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    data_files=[('', ['requirements.txt'])],
)
