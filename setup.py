#!/usr/bin/env python
# -*- Mode: Python; py-indent-offset: 4; coding: utf-8 -*-
# vim: tabstop=4 shiftwidth=4 expandtab

## Copyright (c) 2015, Claudio Luck (Zurich, Switzerland)
##
## Licensed under the terms of the MIT License, see LICENSE file.

from __future__ import print_function

import os
import sys
import codecs
import re
import shutil

from setuptools import setup, Command
from distutils.command.install_data import install_data

PLUGIN = 'eduperson'
PACKAGES = ['ipalib_eduperson']

with codecs.open(os.path.join('.', 'ipalib_eduperson', 'version.py')) as init:
    METADATA = dict(re.findall("__([A-Za-z][A-Za-z0-9_]+)__\s*=\s*'([^']+)'", init.read().decode('utf-8')))

if os.path.exists("README.md"):
    long_description = codecs.open("README.md", "r", "utf-8").read()
else:
    long_description = "See https://github.com/cluck/ipalib-eduperson"

IPASHARE_DIR = '/usr/share/ipa'
try:
    IPALIB_DIR='/usr/lib/python2.7/site-packages/ipalib'
    import ipalib
    IPALIB_DIR=os.path.dirname(ipalib.__file__)
except ImportError:
    pass

class post_install(install_data):
    def run(self):
        install_data.run(self)
	shutil.copy(
            os.path.join(self.install_dir, 'ipalib/plugins/eduperson.py'),
            os.path.join(IPALIB_DIR, 'plugins/eduperson.py'),
        )

extra = {}

setup(
    name = 'ipalib-eduperson',
    packages=PACKAGES,
    version=METADATA['version'],
    description = 'eduPerson plugin for FreeIPA 4',
    long_description = long_description,
    url = 'https://github.com/cluck/ipalib-eduperson',
    author = METADATA['author'],
    author_email = METADATA['author_email'],
    maintainer = 'Claudio Luck',
    maintainer_email = 'claudio.luck@gmail.com',
    license = 'MIT',
    platforms=["any"],
    cmdclass={"install_data": post_install},
    data_files=[
        (os.path.join(IPASHARE_DIR, 'ui/js/plugins', PLUGIN), [PLUGIN+'.js']),
        (os.path.join(IPALIB_DIR, 'plugins'), [PLUGIN+'.py']),  # does not as expected -> post_install
    ],
    entry_points={
        'console_scripts': [
            'eduperson = ipalib_eduperson.commands:eduperson',
        ],
    },
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    **extra
)
