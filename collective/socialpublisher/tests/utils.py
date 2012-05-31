from zope import component

from collective.socialpublisher import interfaces
from collective.socialpublisher.utility import BasePublisherUtility


class FakePublisher(BasePublisherUtility):
	""" a fake publisher just for testing
	"""

	id = "fakepub"
	title = "FakePub"

	def publish(self, text):
		text = '%s says: %s' % (self.account_id, text)
		print text
		return text

	@classmethod
	def get_accounts(self):
		return ['simahawk','simahawktest',]


def register_fake_publisher(name=FakePublisher.id):
	""" register fake publisher
	"""
	component.provideUtility(FakePublisher,
                             name=name,
                             provides=interfaces.ISocialPublisherUtility)
