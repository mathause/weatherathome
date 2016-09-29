#!/usr/bin/env python

from setuptools import setup, find_packages

# get version
with open("weatherathome/version.py") as f:
    l = f.readline().strip().replace(' ', '').replace('"', '')
    version = l.split('=')[1]
    __version__ = version


setup(
    name='weatherathome',
    version=__version__,
    description='functions to work with weatherathome data',
    author='mathause',
    author_email='mathause@ethz.com',
    packages=find_packages(),
    url='https://github.com/mathause/weatherathome',
    install_requires=open('requirements.txt').read().split(),
    long_description=''
)


