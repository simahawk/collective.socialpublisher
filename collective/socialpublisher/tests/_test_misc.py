import unittest2 as unittest

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from collective.socialpublisher.testing import INTEGRATION_TESTING


class TestExample(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        # you'll want to use this to set up anything you need for your tests 
        # below
        pass

    def test_success(self):
        pass