# -*- coding: utf-8 -*-

from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='fetchd',
    version='1.0',
    description='Daemon for fetching files',
    long_description=readme,
    author='Rafał Jagielski',
    author_email='bender@unit22.org',
    url='https://github.com/rjagielski/fetchd',
    license=license,
    packages=find_packages(exclude=('tests',))
)
