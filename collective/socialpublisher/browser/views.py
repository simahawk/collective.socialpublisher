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
        form = self.request.form
        if form.get('autopublish'):
            self.handle_autopublish()
        else:
            self.publish()

    def action_url(self):
        return "%s/%s" % (self.context.absolute_url(),
                          self.__name__)

    def _publish(self, content, publisher, account_id):
        Publisher = getUtility(ISocialPublisherUtility, name=publisher)
        publisher = Publisher(account_id)
        publisher.publish(content)

    def update_message(self, msg, type="info"):
        IStatusMessage(self.request).addStatusMessage(msg,type=type)
        url = self.context.absolute_url()
        self.request.response.redirect(url)

    def publish(self):
        obj = self.context
        selected_publishers = self.request.get('publishers',[])
        if not selected_publishers:
            msg = "select at list one publisher!"
            self.update_message(msg, type="error")
            return
        content = self.get_content()
        text = self.get_content()
        manager = IPublishStorageManager(obj)
        manager.set_text(text)
        selected_accounts = self.request.get('accounts')
        for pub_id in selected_publishers:
            account_id = selected_accounts.get(pub_id)
            manager.set_account(account_id,publisher_id=pub_id)
            self._publish(content, pub_id, account_id)
        msg = 'content published on %s' % ', '.join(selected_publishers)
        self.update_message(msg)

    def get_content(self):
        default = utils.get_text(self.context)
        custom = self.request.get('text','').strip()
        return custom or default

    def prepare_content(self):
        pass

    def handle_autopublish(self):
        form = self.request.form
        obj = self.context
        if form.get('enable'):
            if not IAutoPublishable.providedBy(obj):
                alsoProvides(obj,IAutoPublishable)
                obj.reindexObject(idxs=['object_provides'])
        else:
            if IAutoPublishable.providedBy(obj):
                noLongerProvides(obj,IAutoPublishable)
                obj.reindexObject(idxs=['object_provides'])
        msg = 'Auto-publish updated'
        self.update_message(msg)


class AutoPublish(Publish):

    @property
    def catalog(self):
        return getToolByName(self.context,'portal_catalog')

    def publish(self):
        end = datetime.datetime.now() - datetime.timedelta(1)
        # TODO: make query dinamyc per-type
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
