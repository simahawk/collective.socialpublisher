from persistent.dict import PersistentDict

from zope import component
from zope import interface

from zope.annotation.interfaces import IAnnotations

from collective.socialpublisher.interfaces import IAutoPublishable
from collective.socialpublisher.interfaces import IPublishStorageManager

KEY = 'collective.socialpublisher:publish-settings'


class Manager(object):
	interface.implements(IPublishStorageManager)
	component.adapts(IAutoPublishable)

	def __init__(self, context):
		self.context = context
		annotations = IAnnotations(self.context)
		annotations.setdefault(KEY,PersistentDict())
		self.storage = annotations[KEY]

	def _set_account(self, account_type, account_id):
		self.storage[account_type] = account_id

	def set_account(self, account_id, account_type='twitter'):
		self._set_account(account_type, account_id)

	def _get_account(self, account_type):
		return self.storage.get(account_type)

	def get_twitter_account(self):
		acc_type = 'twitter'
		return self._get_account(acc_type)

	def set_text(self, txt):
		self.storage['text'] = txt

	def get_text(self):
		return self.storage.get('text')

