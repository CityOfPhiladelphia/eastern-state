#!/usr/bin/env python

from distutils.core import setup

setup(
    name='Eastern-State',
    version='0.1dev',
    packages=['eastern_state',],
    description='A secure place to store your environment secrets',
    long_description=open('README.md').read(),
    install_requires=[
        'boto3==1.4.4',
        'click==6.7',
        'PyYAML==3.12'
    ],
    entry_points={
        'console_scripts': [
            'eastern_state=eastern_state:main',
        ],
    }
)
