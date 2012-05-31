from zope import interface
from zope import schema

from zope.annotation.interfaces import IAttributeAnnotatable

from collective.socialpublisher import _


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

class IGlobalSettings(interface.Interface):
    """ global settings
    """

    autopublish_enabled = schema.Bool(
        title=_("Auto-publish enabled"),
        description = _(u"If disabled the cron will not publish anything."),
        default = False
    )

# XXX: this should be used to mark content type klasses on the fly
# but I can't find a clean way to do that since it seems there's no safe way
# to get the klass of the content type. 

    # enabled_content_types = schema.List(
 #        title = _(u'Publishable content types'),
 #        required = False,
 #        default = [],
 #        description = _(u"A list of types can be pusblished"),
 #        value_type = schema.Choice(
 #          title=_(u"Content types"),
 #            source="plone.app.vocabularies.ReallyUserFriendlyTypes"
 #            )
 #        )