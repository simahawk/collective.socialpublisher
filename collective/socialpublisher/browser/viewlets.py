from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase
from zope.component import getMultiAdapter
from Products.CMFCore.utils import getToolByName
from plone.memoize.view import memoize

try:
    import Products.cron4plone
    HAS_CRON4PLONE = True
except ImportError:
    HAS_CRON4PLONE = False

from collective.socialpublisher.interfaces import IAutoPublishable
from collective.socialpublisher.interfaces import IPublishStorageManager
from collective.socialpublisher.config import AUTOPUBLISHABLE_CONTENTTYPES
from collective.socialpublisher import utils


class Social(ViewletBase):
    
    render = ViewPageTemplateFile('viewlet_social.pt')
    
    def available(self):
        return not self.context._at_creation_flag
        
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
            selected = None
            if manager:
                selected = manager.get_account(pub.id)
            accounts = pub.get_accounts()
            res[pub.id] = [
                            dict(id = x,
                                 selected = x == selected)
                            for x in accounts.keys()
                        ]
        return res

    def get_text(self):
        manager = IPublishStorageManager(self.context, None)
        saved = manager.get_text()
        default = utils.get_text(self.context)
        return saved or default

    @property
    def show_cron_info(self):
        return HAS_CRON4PLONE

    @property
    def cron(self):
        return self._get_cron()

    @memoize
    def _get_cron(self):
        cron = None
        if HAS_CRON4PLONE:
            tool = getToolByName(self.context,'CronTool',None)
            if tool is not None:
                schedule = None
                crondata = tool._getCronData()
                # [{'expression': u'portal/@@social-auto-publish', 
                # 'id': 0, 'schedule': [u'*', u'*', u'*', u'*']}]
                for item in crondata:
                    if '@@social-auto-publish' in item.get('expression',''):
                        schedule = item.get('schedule')
                        break
                if schedule is not None:
                    legend = ('min','hour', 'day of month', 'month')
                    cron = ', '.join([': '.join((k,v)) for k,v in  zip(legend,schedule)])
        return cron