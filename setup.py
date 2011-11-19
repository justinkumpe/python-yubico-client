#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re
import sys

from glob import glob
from os.path import splitext, basename, join as pjoin
from unittest import TextTestRunner, TestLoader

from distutils.core import setup
from distutils.core import Command

TEST_PATHS = ['tests']

pre_python26 = (sys.version_info[0] == 2 and sys.version_info[1] < 6)

version_re = re.compile(
    r'__version__ = (\(.*?\))')

cwd = os.path.dirname(os.path.abspath(__file__))
fp = open(os.path.join(cwd, 'yubico', '__init__.py'))

version = None
for line in fp:
    match = version_re.search(line)
    if match:
        version = eval(match.group(1))
        break
else:
    raise Exception('Cannot find version in __init__.py')
fp.close()


class TestCommand(Command):
    description = 'run test suite'
    user_options = []

    def initialize_options(self):
        THIS_DIR = os.path.abspath(os.path.split(__file__)[0])
        sys.path.insert(0, THIS_DIR)
        for test_path in TEST_PATHS:
            sys.path.insert(0, pjoin(THIS_DIR, test_path))
        self._dir = os.getcwd()

    def finalize_options(self):
        pass

    def run(self):
        status = self._run_tests()
        sys.exit(status)

    def _run_tests(self):
        testfiles = []
        for test_path in TEST_PATHS:
            for t in glob(pjoin(self._dir, test_path, 'test_*.py')):
                testfiles.append('.'.join(
                    [test_path.replace('/', '.'), splitext(basename(t))[0]]))

        tests = TestLoader().loadTestsFromNames(testfiles)

        t = TextTestRunner(verbosity=2)
        res = t.run(tests)
        return not res.wasSuccessful()


setup(name='yubico',
      version='.' . join(map(str, version)),
      description='Python Yubico Client',
      author='Tomaž Muraus',
      author_email='tomaz+pypi@tomaz.me',
      license='BSD',
      url='http://github.com/Kami/python-yubico-client/',
      download_url='http://github.com/Kami/python-yubico-client/downloads/',
      packages=['yubico'],
      provides=['yubico'],
      requires=([], ['ssl'],)[pre_python26],
      cmdclass={
          'test': TestCommand,
      },


      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Security',
          'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
