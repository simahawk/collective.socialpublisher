from persistent.dict import PersistentDict

from zope import component
from zope import interface

from zope.annotation.interfaces import IAnnotations

from collective.socialpublisher.interfaces import IPublishable
from collective.socialpublisher.interfaces import IPublishStorageManager

KEY = 'collective.socialpublisher:publish-settings'


class Manager(object):
    interface.implements(IPublishStorageManager)
    component.adapts(IPublishable)

    def __init__(self, context):
        self.context = context

    @property
    def _annotations(self):
        return IAnnotations(self.context)
    
    @property
    def storage(self):
        if KEY not in self._annotations:
            self._reset_storage()
        return self._annotations[KEY]

    def _reset_storage(self):
        self._annotations[KEY] = PersistentDict()
        # set up sub keys
        self._annotations[KEY]['accounts'] = {}
        self._annotations[KEY]['text'] = ""

    def get_accounts(self):
        return self.storage['accounts']

    def _set_account(self, publisher_id, account_id):
        self.storage['accounts'][publisher_id] = account_id

    def set_account(self, publisher_id, account_id):
        self._set_account(publisher_id, account_id)

    def _get_account(self, publisher_id):
        return self.storage['accounts'].get(publisher_id)

    def get_account(self, publisher_id):
        return self._get_account(publisher_id)

    def set_text(self, txt):
        self.storage['text'] = txt

    def get_text(self):
        return self.storage.get('text','')

