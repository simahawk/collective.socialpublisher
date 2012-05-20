Introduction
============

Provides a viewlet (and under-the-hood machinery) for managers that allows to publish contents to social networks (only twitter ATM). Social publication can be automated by enabling it per-content.

To enable the viewlet just mark the content-type you want with `collective.socialpublisher.interfaces.IPublishable`. You can do it from ZMI or trough ZMCL::

	<class class="Products.ATContentTypes.content.event.ATEvent">
    	<implements interface="collectinve.socialpublisher.interfaces.IPublishable" />
    </class>

    NOTE: this is already done by the package in this alpha stage.

Twitter accounts management is done by `collective.twitter.accounts`.

You can provide a publisher by registeriing an utility providing `collective.socialpublisher.interfaces.ISocialPublisherUtility`. See `collective.socialpublisher.utility` for details.

To enable auto-publishing you have to enable it per-content (waiting for global configuration) and you have to create a cron the calls `@@social-auto-publish`. You can do it using `Products.cron4plone` or trough buildout like this::

	[instance]
	...
	zope-conf-additional =
	  <clock-server>
	      method /plonesite/@@social-auto-publish
	      period 1000
	      user admin
	      password admin
	  </clock-server>

See also http://collective-docs.readthedocs.org/en/latest/misc/asyncronoustasks.html.

    