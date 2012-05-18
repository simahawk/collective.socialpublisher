import tweepy

from zope.interface import implements
from zope.interface import classProvides

from collective.socialpublisher.interfaces import ISocialPublisherUtility
from collective.socialpublisher.interfaces import ISocialPublisher


class BasePublisherUtility(object):
	classProvides(ISocialPublisherUtility)
	implements(ISocialPublisher)


	def __init__(self, **kw):
		self.consumer_key = kw.get('consumer_key')
		self.consumer_secret = kw.get('consumer_secret')
		self.oauth_token = kw.get('oauth_token')
		self.oauth_token_secret = kw.get('oauth_token_secret')
		self.api = self._get_api()

	def _get_api(self):
		raise NotImplemented()

	def publish(self, text):
		raise NotImplemented()


class TwitterPublisher(BasePublisherUtility):

	def _get_api(self):
		auth = tweepy.OAuthHandler(self.consumer_key,self.consumer_secret)
		auth.set_access_token(self.oauth_token,self.oauth_token_secret)
		api = tweepy.API(auth)
		return api

	def publish(self, text):
 		self.api.update_status(text)
