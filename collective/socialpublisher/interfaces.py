from zope import interface
from zope import schema

from zope.annotation.interfaces import IAttributeAnnotatable

from collective.socialpublisher import _


class IAutoPublishable(IAttributeAnnotatable):
    """ marker interface for objects that are allowed
    to be auto-published
    """


class IPublishable(IAttributeAnnotatable):
    """ marker interface for objects that are allowed
    to be published
    """


class IPublishStorageManager(interface.Interface):
    """ adapter for managing settings storage on IPublishable objects
    """

    def get_accounts():
        """ returns adict of publisher/account mapping
        """

    def set_account(publisher_id, account_id):
        """ store publisher/account mapping

        publisher_id -- id of a registered publisher
        account_id -- id of an account to be used with the publisher
        """

    def get_account(publisher_id):
        """ returns account id for the given publisher

        publisher_id -- id of a registered publisher
        """

    def set_text(txt):
        """ store the text to be published

        txt -- multiline text
        """

    def get_text():
        """ returns the text to be published
        """


class ISocialPublisherUtility(interface.Interface):
    """ utility for publishing
    """


class ISocialPublisher(interface.Interface):
    """ a social publisher
    """

    def publish(text):
        """ publish given text
        """

    def get_accounts():
        """ returns adict containing the accounts registered
        for this publisher
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