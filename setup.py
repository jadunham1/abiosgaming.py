import sys
import os
import re

from setuptools import setup
from setuptools.command.test import test as TestCommand

kwargs = {}
requires = []
packages = [
    "abiosgaming",
]

__version__ = ''
with open('abiosgaming/__about__.py', 'r') as fd:
    reg = re.compile(r'__version__ = [\'"]([^\'"]*)[\'"]')
    for line in fd:
        m = reg.match(line)
        if m:
            __version__ = m.group(1)
            break

if not __version__:
    raise RuntimeError('Cannot find version information')

class PyTest(TestCommand):
    user_options = [('pytest-args=', 'a', "Arguments to pass to py.test")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)

setup(
    name = "abiosgaming.py",
    description = 'Client for interacting with the AbiosGaming API',
    author = 'Jeff Dunham',
    author_email = 'jeffrey.a.dunham@gmail.com',
    version = __version__,
    packages = packages,
    setup_requires=[
        'pytest-runner',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
    ],
    tests_require=[
        'pytest',
    ],
)
