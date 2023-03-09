#!/usr/bin/env python

import os
import re

from setuptools import setup, find_packages


# Read properties from __init__.py
with open(os.path.join(os.path.dirname(__file__), 'pylinkam', '__init__.py')) as file_init:
    content_init = file_init.read()

    version = re.search("__version__ = '([^']+)'", content_init).group(1)

    author = re.search("__author__ = '([^']+)'", content_init).group(1)

    maintainer = re.search("__maintainer__ = '([^']+)'", content_init).group(1)
    maintainer_email = re.search("__email__ = '([^']+)'", content_init).group(1)


setup(
    name='pylinkam',
    version=version,
    description='Python bindings for the official Linkam SDK',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author=author,
    maintainer=maintainer,
    maintainer_email=maintainer_email,
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: System :: Hardware',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    license='GPLv3',
    platforms='any'
)
