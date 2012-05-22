from zope.i18nmessageid import MessageFactory

socialPublisherMF = MessageFactory('collective.socialpublisher')
_ = socialPublisherMF


def initialize(context):
    """Initializer called when used as a Zope 2 product."""
