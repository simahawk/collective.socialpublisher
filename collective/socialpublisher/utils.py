# imports for tiny url call
from urllib import urlencode
from urllib2 import urlopen, HTTPError, URLError

from zope import component
from zope.component import getUtility
from plone.registry.interfaces import IRegistry

from collective.socialpublisher.interfaces import IPublishStorageManager
from collective.socialpublisher.interfaces import ISocialPublisherUtility
from collective.socialpublisher.interfaces import IGlobalSettings


def getTinyURL(url):
    """ returns shotend url or None """  
    TINYURL = 'http://tinyurl.com/api-create.php'
    linkdata = urlencode(dict(url=url))
    try:
        link = urlopen( TINYURL, data=linkdata ).read().strip()
    except URLError:
        # there was an error
        link = None
    return link

def get_publishers():
    gsm = component.getGlobalSiteManager()
    publishers = gsm.getAllUtilitiesRegisteredFor(ISocialPublisherUtility)
    return publishers

def get_text(obj):
    # XXX: make this smarter (using per-type adapters?)
    LIMIT = 140
    manager = IPublishStorageManager(obj)
    if manager.get_text():
        txt = manager.get_text()[:LIMIT]
    else:
        txt = obj.Title()
        link = obj.absolute_url()
        # XXX: handle this is an smart way
        # short_link = getTinyURL(link)
        short_link = None 
        if short_link:
            link = short_link
        else:
            short_link = link
        available_chars = LIMIT - (len(short_link)+1)
        txt = "%s %s" % (txt[:available_chars],short_link)
    return txt


def get_global_settings():
    registry = component.getUtility(IRegistry)
    return registry.forInterface(IGlobalSettings)