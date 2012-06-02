import tweepy

from zope import component

from zope.interface import implements
from zope.interface import classProvides

from plone.registry.interfaces import IRegistry

from collective.socialpublisher.interfaces import ISocialPublisherUtility
from collective.socialpublisher.interfaces import ISocialPublisher


class BasePublisherUtility(object):
	classProvides(ISocialPublisherUtility)
	implements(ISocialPublisher)

	id = ""
	title = ""

	def __init__(self, account_id):
		""" initialize your stuff here
		"""
		self.account_id = account_id

	def publish(self, text):
		raise NotImplemented()

	def get_accounts(self):
		return NotImplemented()


class TwitterPublisher(BasePublisherUtility):

	id="twitter"
	title="Twitter"

	def __init__(self, account_id):
		assert account_id
		self.account_id = account_id
		account = self.get_account(account_id)
		self.consumer_key = account.get('consumer_key')
		self.consumer_secret = account.get('consumer_secret')
		self.oauth_token = account.get('oauth_token')
		self.oauth_token_secret = account.get('oauth_token_secret')
		self.api = self._get_api()

	def _get_api(self):
		auth = tweepy.OAuthHandler(self.consumer_key,self.consumer_secret)
		auth.set_access_token(self.oauth_token,self.oauth_token_secret)
		api = tweepy.API(auth)
		return api

	def publish(self, text):
 		self.api.update_status(text)

 	def get_account(self, account_id):
 		return self.get_accounts()[account_id]

 	@classmethod
 	def get_accounts(cls):
		registry = component.getUtility(IRegistry)
		accounts = registry.get('collective.twitter.accounts', [])
		return accounts
