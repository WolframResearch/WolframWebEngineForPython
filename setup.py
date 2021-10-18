

from __future__ import absolute_import, print_function, unicode_literals

import sys

try:
    from setuptools import setup, find_packages
except ImportError:
    sys.stderr.write("""Could not import setuptools or your version
of the package is out of date.

Make sure you have pip and setuptools installed and upgraded and try again:
    $ python -m pip install --upgrade pip setuptools
    $ python setup.py install

""")

def load_tests():
    from wolframwebengine.cli.commands.test import Command as TestCommand
    TestCommand().handle()

setup(
    name = 'wolframwebengine',
    version = '1.0.3',
    description = 'A Python library with various tools to start a wolfram engine a server content.',
    keywords=['Wolfram Language', 'Wolfram Desktop', 'Mathematica', 'Web Development', 'Wolfram Web Engine'],
    author = 'Wolfram Research, Riccardo Di Virgilio',
    author_email = 'support@wolfram.com, riccardod@wolfram.com',
    packages=find_packages(),
    test_suite='setup.load_tests',
    python_requires='>=3.5.3',
    include_package_data=True,
    install_requires = [
        'wolframclient>=1.1.0',
        'aiohttp>=3.5.4'
    ],
    project_urls={
        'Source code': 'https://github.com/WolframResearch/WolframWebEngineForPython',
        'Wolfram Research': 'https://www.wolfram.com',
    },
    classifiers = [
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries"
    ],
    entry_points={
        'console_scripts': [
            'wolframwebengine = wolframwebengine.__main__:main',
        ]
    }
)
