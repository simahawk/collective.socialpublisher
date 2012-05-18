# imports for tiny url call
from urllib import urlencode
from urllib2 import urlopen, HTTPError, URLError

from zope import component

from plone.registry.interfaces import IRegistry

from collective.socialpublisher.interfaces import IPublishStorageManager


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

def get_twitter_accounts():
	registry = component.getUtility(IRegistry)
	accounts = registry.get('collective.twitter.accounts', [])
	return accounts

def get_text(obj):
    LIMIT = 140
    manager = IPublishStorageManager(obj)
    if manager.get_text():
        txt = manager.get_text()[:LIMIT]
    else:
        txt = obj.Title()
        url = obj.absolute_url()
        short_link = getTinyURL(url)
        available_chars = LIMIT - (len(short_link)+1)
        txt = "%s %s norepeat" % (txt[:available_chars],short_link)
    return txt