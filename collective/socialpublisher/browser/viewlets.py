from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize

from collective.socialpublisher.interfaces import IAutoPublishable
from collective.socialpublisher.interfaces import IPublishStorageManager
from collective.socialpublisher.config import AUTOPUBLISHABLE_CONTENTTYPES
from collective.socialpublisher import utils


class Social(ViewletBase):
    
    render = ViewPageTemplateFile('viewlet_social.pt')
    
    def update(self):
        portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
        self.navigation_root_url = portal_state.navigation_root_url()
        portal = portal_state.portal()
        self.portal_title = portal_state.portal_title()
        
    def action_url(self):
    	return self.context.absolute_url() +'/@@social-publish'

    def auto_publish_allowed(self):
    	return self.context.meta_type in AUTOPUBLISHABLE_CONTENTTYPES

    def auto_publish_enabled(self):
    	return IAutoPublishable.providedBy(self.context)

    def has_accounts(self):
        return bool(utils.get_twitter_accounts().keys())

    @property
    def twitter_accounts(self):
        manager = IPublishStorageManager(self.context, None)
        selected = ''
        if manager:
            selected = manager.get_twitter_account()
        accounts = utils.get_twitter_accounts().keys()
        return [
            dict(id = x,
                selected = x == selected)
            for x in accounts
        ]