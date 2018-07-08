"""wheel setup for Prosper common utilities"""
import codecs
import importlib
import os

from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand

HERE = os.path.abspath(os.path.dirname(__file__))

__package_name__ = 'vincent'
__library_name__ = 'vincent-lexicon'

def get_version(package_name):
    """find __version__ for making package

    Args:
        package_name (str): path to _version.py folder (abspath > relpath)

    Returns:
        str: __version__ value

    """
    module = package_name + '._version'
    package = importlib.import_module(module)

    version = package.__version__

    return version


class PyTest(TestCommand):
    """PyTest cmdclass hook for test-at-buildtime functionality

    http://doc.pytest.org/en/latest/goodpractices.html#manual-integration

    """
    user_options = [('pytest-args=', 'a', 'Arguments to pass to pytest')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = [
            'tests',
            '-rx',
            '--cov=' + __package_name__,
            '--cov=' + __package_name__ + '_crons',
            '--cov-report=term-missing',
            '--cov-config=.coveragerc',
        ]

    def run_tests(self):
        import shlex
        import pytest
        pytest_commands = []
        try:
            pytest_commands = shlex.split(self.pytest_args)
        except AttributeError:
            pytest_commands = self.pytest_args
        errno = pytest.main(pytest_commands)
        exit(errno)

class TravisTest(PyTest):
    """wrapper for quick-testing for devs"""
    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = [
            'tests',
            '-rx',
            '--junitxml=junit.xml',
            '--cov=' + __package_name__,
            '--cov=' + __package_name__ + '_crons',
            '--cov-report=term-missing',
            '--cov-config=.coveragerc',
        ]

with codecs.open('README.rst', 'r', 'utf-8') as readme_fh:
    README = readme_fh.read()

setup(
    name=__library_name__,
    version=get_version(__package_name__),
    description='NLP sentiment analysis for corperate-speak',
    long_description=README,
    author='John Purcell',
    author_email='jpurcell.ee@gmail.com',
    url='https://github.com/EVEProsper/' + __library_name__,
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
    packages=find_packages(),
    python_requires='>=3.6',
    include_package_data=True,
    package_data={
        '': ['LICENSE', 'README.rst'],
        __library_name__: ['version.txt'],
        'vincent_crons': ['app.cfg'],
    },
    entry_points={
        'console_scripts': [
            'GetNews=vincent_crons.GetNews:run_main',
        ],
    },
    install_requires=[
        'nltk',
        'pandas',
        'ProsperCommon',
        'ProsperDatareader',
        'plumbum',
        'requests',
    ],
    tests_require=[
        'pytest',
        'pytest_cov',
    ],
    extras_require={
        'dev':[
            'sphinx',
            'sphinxcontrib-napoleon',
            'semantic-version',
            'awscli',
        ]
    },
    cmdclass={
        'test':PyTest,
        'travis': TravisTest,
    },
)
