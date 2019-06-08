#!/usr/bin/env python
# Author: Magic Foundation <support@hologram.io>
#
# Copyright 2018 - Magic Foundation
#
# LICENSE: Distributed under the terms of the MIT License
#

from setuptools import setup, find_packages

setup(
    name='magic_network',
    version=open('version.txt').read().split()[0],
    description='Library for accessing the Magic network',
    long_description='',
    author='Magic Foundation',
    author_email='support@hologram.io',
    packages=find_packages(),
    include_package_data=True,
    install_requires=open('requirements.txt').read().split(),
    setup_requires=["pytest-runner"],
    tests_require=["pytest"],
    scripts=['magic/bin/magic-network'],
    license='MIT'
)
