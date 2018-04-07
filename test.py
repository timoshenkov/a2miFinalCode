"""Unit tests"""
from __future__ import print_function

import unittest
import sys

if sys.version_info.major == 2:
  import mock                # pylint: disable=g-import-not-at-top,unused-import
else:
  from unittest import mock  # pylint: disable=g-import-not-at-top

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO  # pylint: disable=g-import-not-at-top,unused-import

TEST_DYNAMODB_LOCAL = False

_TEST_MODULES = [
    'kvs_test',
    'loader_test',
    'parser_test',
    'querier_test',
]


class TestCase(unittest.TestCase):
    pass


def main():
    """Runs all unit tests."""
    return unittest.main()

if __name__ == '__main__':
    suite = unittest.TestSuite()
    for t in _TEST_MODULES:
        suite.addTest(unittest.defaultTestLoader.loadTestsFromName(t))
    unittest.TextTestRunner().run(suite)
