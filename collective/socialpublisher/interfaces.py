from zope import interface

from zope.annotation.interfaces import IAttributeAnnotatable


class IAutoPublishable(IAttributeAnnotatable):
	""" marker interface
	"""

class IPublishable(IAttributeAnnotatable):
	""" marker interface
	"""

class IPublishStorageManager(interface.Interface):
	""" adapter for storing social publish info
	"""

class ISocialPublisherUtility(interface.Interface):
	""" utility for publishing
	"""

class ISocialPublisher(interface.Interface):
	""" a social publisher
	"""