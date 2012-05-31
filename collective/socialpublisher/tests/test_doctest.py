# -*- coding: utf-8 -*-
import unittest2 as unittest
import doctest

from plone.testing import layered

from collective.socialpublisher.testing import FUNCTIONAL_TESTING


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(
            doctest.DocFileSuite(
                'tests/MANAGER.txt',
                package='collective.socialpublisher',
                optionflags=doctest.REPORT_ONLY_FIRST_FAILURE | 
                        doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS,
            ),
            layer=FUNCTIONAL_TESTING,
        ),
    ])
    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='test_suite')
