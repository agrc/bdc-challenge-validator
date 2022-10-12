#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
setup.py
A module that installs projectname as a module
"""
from glob import glob
from os.path import basename, splitext

from setuptools import find_packages, setup

#: Load version from source file
version = {}
with open('src/validator/version.py') as fp:
    exec(fp.read(), version)

setup(
    name='ugrc-bdc-challenge-validator',
    version=version['__version__'],
    license='MIT',
    description='Project description.',
    author='UGRC',
    author_email='ugrc@utah.gov',
    url='https://github.com/agrc/bdc-challenge-validator',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    py_modules=[splitext(basename(path))[0] for path in glob('src/*.py')],
    include_package_data=True,
    zip_safe=True,
    classifiers=[
        # complete classifier list: http://pypi.python.org/pypi?%3Aaction=list_classifiers
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
    ],
    project_urls={
        'Issue Tracker': 'https://github.com/agrc/python/issues',
    },
    keywords=['gis'],
    install_requires=['arcgis>1.7'],
    extras_require={
        'tests': [
            'pylint-quotes~=0.2',
            'pylint~=2.11',
            'pytest-cov~=3.0',
            'pytest-instafail~=0.4',
            'pytest-isort>=2,<4',
            'pytest-mock~=3.8',
            'pytest-pylint~=0.18',
            'pytest-watch~=4.2',
            'pytest>=6,<8',
            'yapf~=0.31',
        ]
    },
    setup_requires=[
        'pytest-runner',
    ],
    entry_points={'console_scripts': [
        'bdcvalidator = validator.main:main',
    ]},
)
