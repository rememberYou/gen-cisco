#!/usr/bin/env python3

import os
from setuptools import setup, find_packages

try:
    import pypandoc
    long_description = pypandoc.convert('README.md', 'rst')
except(IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name="gen-cisco",
    version="1.2.0",
    description="Generates Cisco scripts based on YAML files",
    author="Terencio Agozzino",
    author_email="terencio.agozzino@gmail.com",
    license="MIT",
    keywords = "cisco ccna generate netacad packettracer python script scripts",
    url="https://github.com/rememberYou/gen-cisco",
    packages=find_packages(),
    long_description=long_description,
    scripts=['gen-cisco.py'],
    install_requires=['click'],
    project_urls={
        'Source': 'https://github.com/rememberYou/gen-cisco',
        'Tracker': 'https://github.com/rememberYou/gen-cisco/issues',
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.1",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3 :: Only",
        "Topic :: Utilities",
    ],
)
