from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from plone.memoize.view import memoize

from collective.socialpublisher.interfaces import IAutoPublishable
from collective.socialpublisher.interfaces import IPublishStorageManager
from collective.socialpublisher.config import AUTOPUBLISHABLE_CONTENTTYPES
from collective.socialpublisher import utils


class Social(ViewletBase):
    
    render = ViewPageTemplateFile('viewlet_social.pt')
    
    def update(self):
        pass
        
    def action_url(self):
        return self.context.absolute_url() +'/@@social-publish'

    def auto_publish_enabled(self):
    	return IAutoPublishable.providedBy(self.context)

    def has_accounts(self):
        has = False
        for pub in self.publishers:
            if pub.get_accounts():
                has = True
                break
        return has

    @property
    def publishers(self):
        return utils.get_publishers()

    @property
    def accounts(self):
        res = {}
        manager = IPublishStorageManager(self.context, None)
        selected = ""
        for pub in self.publishers:
            if manager is None:
                res[pub.id] = []
            else:
                selected = manager.get_account(pub.id)
                accounts = pub.get_accounts()
                res[pub.id] = [
                                dict(id = x,
                                     selected = x == selected)
                                for x in accounts.keys()
                            ]
        return res