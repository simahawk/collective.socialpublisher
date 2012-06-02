# -*- coding: utf8 -*-

import unittest2 as unittest

import DateTime

from zope import component
from zope import interface 

from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

from plone.registry.interfaces import IRegistry

from collective.socialpublisher.testing import INTEGRATION_TESTING
from collective.socialpublisher.tests import utils as test_utils
from collective.socialpublisher.interfaces import ISocialPublisherUtility
from collective.socialpublisher.interfaces import ISocialPublisher
from collective.socialpublisher.interfaces import IPublishStorageManager
from collective.socialpublisher.interfaces import IAutoPublishable
from collective.socialpublisher import utils


class TestExample(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        # you'll want to use this to set up anything you need for your tests 
        # below
        self.portal = self.layer['portal']

    def test_globalsettings(self):
        settings = utils.get_global_settings()
        # autopublish must be disabled by default
        self.assertFalse(settings.autopublish_enabled)

    def test_publisher(self):
        test_utils.register_fake_publisher()
        utility = component.queryUtility(ISocialPublisherUtility,
                                         name=test_utils.FakePublisher.id)
        self.assertFalse(utility is None)

        # make sure we get a publisher
        publisher = utility('simahawk')
        self.assertTrue(ISocialPublisher.providedBy(publisher))

        # and that it publish what we want
        text = 'Lorem ipsum foo bar!'
        result = publisher.publish(text)
        expected = 'simahawk says: ' + text
        self.assertEqual(result,expected)
    
    def create_event(self):
        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        evid = self.portal.invokeFactory('Event','event')
        event = self.portal[evid]
        event.start = DateTime.DateTime()
        event.end = DateTime.DateTime() + 4
        title = 'Great event'
        event.setTitle(title)
        text = 'Something awesome is going on!'
        event.setText(text)
        return event

    def test_get_text(self):
        event = self.create_event()
        txt = utils.get_text(event)
        expected = 'Great event http://nohost/plone/event'
        self.assertTrue(expected,txt)

    def test_publish(self):
        test_utils.register_fake_publisher()
        utility = component.queryUtility(ISocialPublisherUtility,
                                         name=test_utils.FakePublisher.id)
        # let's create an event
        event = self.create_event()
        # and get its manager
        manager = IPublishStorageManager(event)
        # we must have empty values here
        self.assertEqual(manager.get_accounts(),{})
        self.assertEqual(manager.get_text(),'')

        # we can now publish it using `social-publish` view
        view = event.restrictedTraverse('@@social-publish')
        publishers = [test_utils.FakePublisher.id]
        accounts = {test_utils.FakePublisher.id:'simahawk'}
        result = view.publish(publishers=publishers,accounts=accounts)
        # we expect the content of the publication to be equal `get_text` result
        # and the publisher/account mapping matching the one we pass to the publisher
        expected = {'content': 'Great event http://nohost/plone/event', 'fakepub': 'simahawk'}
        self.assertEqual(result,expected)
        # publisher/account mapping is saved by default by the publishing view
        self.assertEqual(manager.get_accounts(),{'fakepub': 'simahawk'})

    def test_autopublish(self):
        test_utils.register_fake_publisher()
        utility = component.queryUtility(ISocialPublisherUtility,
                                         name=test_utils.FakePublisher.id)
        # let's create an event
        event = self.create_event()

        view = self.portal.restrictedTraverse('@@social-auto-publish')
        # manager.set_account(test_utils.FakePublisher.id,'simahawk')
        # the event is not auto-publish enabled so we must get no items
        self.assertEqual(len(view.get_items()),0)        
        interface.alsoProvides(event, IAutoPublishable)
        event.reindexObject(idxs=['object_provides'])
        self.assertEqual(len(view.get_items()),1) 
        # but since auto-publish is disabled by default 
        # we should get disabled message on publish
        result = view.publish()
        self.assertEqual(result,view.msg_autopublish_disabled)
        # let's enable it
        registry = utils.get_global_settings()
        registry.autopublish_enabled = True
        # and retry
        result = view.publish()
        self.assertEqual(result,view.msg_autopublish_done)


def test_suite():
    return unittest.defaultTestLoader.loadTestsFromName(__name__)