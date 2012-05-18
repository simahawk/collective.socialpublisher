import datetime
from twitter import Twitter

from zope.component import getUtility

from zope.interface import implements
from zope.interface import alsoProvides
from zope.interface import noLongerProvides

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from Products.statusmessages.interfaces import IStatusMessage

from collective.socialpublisher.interfaces import IAutoPublishable
from collective.socialpublisher.interfaces import IPublishStorageManager
from collective.socialpublisher.interfaces import ISocialPublisherUtility
from collective.socialpublisher import utils


class Publish(BrowserView):

    def __call__(self):
        return self.publish()

    def action_url(self):
        return "%s/%s" % (self.context.absolute_url(),
                          self.__name__)

    def _publish(self, content, where='twitter', account_id=""):
        accounts = utils.get_twitter_accounts()
        account = accounts.get(account_id, {})
        results = []

        if account:
            Publisher = getUtility(ISocialPublisherUtility, name=where)
            publisher = Publisher(**account)
            publisher.publish(content)
        else:
            print "can't find account %s" % account_id

    def publish(self):
        obj = self.context
        if self.request.get('make_autopublishable',0)==1:
            if not IAutoPublishable.providedBy(obj):
                alsoProvides(obj,IAutoPublishable)
                obj.reindexObject(idxs=['object_provides'])
        else:
            if IAutoPublishable.providedBy(obj):
                obj.reindexObject(idxs=['object_provides'])
                noLongerProvides(obj,IAutoPublishable)
        where = self.request.get('where')
        if where is not None:
            username = self.request.get('twitter_account')
            manager = IPublishStorageManager(obj)
            manager.set_account(username,account_type='twitter')
            content = self.get_content()
            self._publish(content, account_id=username)
            msg = 'content published'
        else:
            msg = 'done'
        IStatusMessage(self.request).addStatusMessage(msg)
        url = self.context.absolute_url()
        self.request.response.redirect(url)

    def get_content(self):
        return utils.get_text(self.context)

    def prepare_content(self):
        pass


class AutoPublish(Publish):

    @property
    def catalog(self):
        return getToolByName(self.context,'portal_catalog')

    def publish(self):
        end = datetime.datetime.now() - datetime.timedelta(1)
        query = dict(
            portal_type="Event",
            end = dict(query=end,range='min')
        )
        brains = self.catalog(query)
        for brain in brains:
            obj = brain.getObject()
            content = utils.get_text(obj)
            manager = IPublishStorageManager(obj)
            account_id = manager.get_twitter_account()
            self._publish(content,account_id=account_id)
