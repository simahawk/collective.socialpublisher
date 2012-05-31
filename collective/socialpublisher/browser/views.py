import datetime
import logging

from zope.component import getUtility

from zope.interface import implements
from zope.interface import alsoProvides
from zope.interface import noLongerProvides

from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

from Products.statusmessages.interfaces import IStatusMessage

from plone.registry.interfaces import IRegistry

from collective.socialpublisher.interfaces import IGlobalSettings
from collective.socialpublisher.interfaces import IAutoPublishable
from collective.socialpublisher.interfaces import IPublishStorageManager
from collective.socialpublisher.interfaces import ISocialPublisherUtility
from collective.socialpublisher import utils
from collective.socialpublisher import _


class Publish(BrowserView):

    def __call__(self):
        form = self.request.form
        if form.get('autopublish'):
            self.handle_autopublish()
        elif form.get('update'):
            self.update_settings()
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
        url = self.context.absolute_url() +'?submitted=1'
        self.request.response.redirect(url)

    def _update_settings(self):
        obj = self.context
        selected_publishers = self.request.get('publishers',[])
        manager = IPublishStorageManager(obj)
        custom_text = self.request.get('text','').strip()
        if not self.request.get('one_shot_text'):
            manager.set_text(custom_text)
        selected_accounts = self.request.get('accounts')
        for pub in selected_publishers:
            account_id = selected_accounts.get(pub)
            manager.set_account(pub,account_id)

    def update_settings(self):
        self._update_settings()
        msg = _(u"Settings updated")
        self.update_message(msg)

    def publish(self):
        obj = self.context
        selected_publishers = self.request.get('publishers',[])
        if not selected_publishers:
            msg = _(u"Select at list one publisher!")
            self.update_message(msg, type="error")
            return
        self._update_settings()
        content = self.get_content()
        manager = IPublishStorageManager(obj)
        if manager.get_text() and not self.request.get('one_shot_text'):
            content = manager.get_text()
        selected_accounts = self.request.get('accounts')
        for pub in selected_publishers:
            account_id = selected_accounts.get(pub)
            self._publish(content, pub, account_id)
        msg = _(u'content_published',
                default=u"Content published on ${published_on}",
                mapping={'published_on': ', '.join(selected_publishers) })
        translated = self.context.translate(msg)
        self.update_message(translated)

    def get_content(self):
        default = utils.get_text(self.context)
        custom = self.request.get('text','').strip()
        return custom or default

    def prepare_content(self):
        pass

    def handle_autopublish(self):
        form = self.request.form
        obj = self.context
        changed = False
        if form.get('enable'):
            if not IAutoPublishable.providedBy(obj):
                alsoProvides(obj,IAutoPublishable)
                msg = _('Auto-publish enabled')
                changed = True
        else:
            if IAutoPublishable.providedBy(obj):
                noLongerProvides(obj,IAutoPublishable)
                msg = _('Auto-publish disabled')
                changed = True
        if changed:
            obj.reindexObject(idxs=['object_provides'])
            self.update_message(msg)


autopublish_log = logging.getLogger('[AutoPublisher]')

class AutoPublish(Publish):

    @property
    def catalog(self):
        return getToolByName(self.context,'portal_catalog')

    def publish(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(IGlobalSettings)
        if not settings.autopublish_enabled:
            autopublish_log.info('Auto-publishing disabled globally')
            return
        end = datetime.datetime.now() - datetime.timedelta(1)
        # TODO: make query dinamyc per-type
        # but then: how to get all enabled types in a smart way?
        # see also ..interfaces.IGlobalSettings
        query = dict(
            portal_type="Event",
            end = dict(query=end,range='min'),
            object_provides=IAutoPublishable.__identifier__,
        )
        brains = self.catalog(query)
        for brain in brains:
            obj = brain.getObject()
            manager = IPublishStorageManager(obj)
            # XXX: we should delegate default text get to manager (?)
            content = manager.get_text() or utils.get_text(obj)
            for publisher,account_id in manager.get_accounts().items():
                self._publish(content, publisher, account_id=account_id)
