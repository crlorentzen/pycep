"""The pycep python package."""
# coding=utf-8
import os
from setuptools import setup, find_packages
from pycep import __version__

setup(
    name="pycep",
    version=__version__,
    packages=find_packages(exclude=['docs', 'tests', 'tools', 'utils']),
    url="https://github.com/simspace/pycep/",
    license='Apache 2.0',
    author="Wyatt Roersma",
    author_email="wyatt@simspace.com",
    description="This is the Python linting library for CEPs.",
    include_package_data=True,
    zip_safe=False,
    classifiers=['Development Status :: 4 - Beta',
                 'Intended Audience :: Developers',
                 'License :: OSI Approved :: Apache 2.0',
                 'Programming Language :: Python :: 3.7'],
    package_data={
        'pycep': ['*.txt'],  'pycep:ceps': ['*.*'], 'pycep:data': ['*.txt']
    },
    scripts=['pycep/cepcli.py'],
    )
