# -*- coding: utf-8 -*-
import sys

from setuptools import setup
from setuptools.command.test import test as TestCommand

requires = ['click']
tests_require = ['pytest', 'pytest-cache', 'pytest-cov']


class PyTest(TestCommand):
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
    name="mmetering-cli",
    version='0.1.0',
    description="Command line interface for MMetering",
    long_description="\n\n".join([open("README.rst").read()]),
    license='MIT',
    author="Christoph Sonntag",
    author_email="info@chrisonntag.com",
    url="https://mmetering.chrisonntag.com/",
    packages=['src'],
    install_requires=requires,
    entry_points={'console_scripts': [
        'mmetering-cli = src.cli:main']},
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Framework :: Django :: 1.10',
        'Environment :: Console',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: Implementation :: CPython'],
    extras_require={'test': tests_require},
    cmdclass={'test': PyTest})
