#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from setuptools import setup
from pip.req import parse_requirements

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()

with open('requirements.txt') as requirements:
    REQUIRES = requirements.read().splitlines()


install_reqs = parse_requirements('./requirements.txt', session='hack')
reqs = [str(ir.req) for ir in install_reqs]



setup(
    name='Fprint API',
    version='0.0.1',
    license='GPLv3+',
    description=(
        'Fprint API for Open Broadcast Playlists'
    ),
    long_description=README,
    url='https://weblate.org/',
    author='Jonas Ohrstrom',
    author_email='ohrstrom@gmail.com',
    install_requires=reqs,
    zip_safe=False,
    extras_require={
        'Mercurial': ['Mercurial>=2.8'],
        'Unicode': ['pyuca>=1.1', 'python-bidi>=0.4.0', 'chardet'],
        'Avatars': [
            'pyLibravatar',
            'pydns' if sys.version_info[0] == 2 else 'py3dns'
        ],
        'Android': ['Babel'],
        'YAML': ['PyYAML>=3.0'],
        'OCR': ['tesserocr>=1.2'],
    },
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: '
        'GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: OS Independent',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Topic :: Internet :: WWW/HTTP',
    ],
    entry_points={
        'console_scripts': [
            'fprint-api = app.runner:main',
        ],
    },
    tests_require=(
        'selenium',
        'httpretty',
    ),
    test_suite='runtests.runtests',

)
