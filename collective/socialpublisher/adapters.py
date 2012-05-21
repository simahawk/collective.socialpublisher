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
		annotations = IAnnotations(self.context)
		annotations.setdefault(KEY,PersistentDict())
		self.storage = annotations[KEY]

	def _set_account(self, publisher_id, account_id):
		self.storage[publisher_id] = account_id

	def set_account(self, account_id, publisher_id):
		# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXs
		# remove twitter, this stuff should be indipendent
		# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
		self._set_account(publisher_id, account_id)

	def _get_account(self, publisher_id):
		return self.storage.get(publisher_id)

	def get_account(self, publisher_id):
		return self._get_account(publisher_id)

	def set_text(self, txt):
		self.storage['text'] = txt

	def get_text(self):
		return self.storage.get('text','')

