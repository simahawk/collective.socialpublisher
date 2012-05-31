from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import PloneSandboxLayer
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting
from plone.app.testing import applyProfile

from plone.testing import z2

from zope.configuration import xmlconfig

PACKAGENAME = 'collective.socialpublisher'

class CollectiveSocialpublisher(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE, )

    def setUpZope(self, app, configurationContext):
        # Load ZCML for this package
        import collective.socialpublisher
        xmlconfig.file('configure.zcml',
                       collective.socialpublisher,
                       context=configurationContext)
        z2.installProduct(app, 'collective.socialpublisher')


    def setUpPloneSite(self, portal):
        self.applyProfile(portal, PACKAGENAME+':default')

    def tearDownZope(self, app):
        # Uninstall product
        z2.uninstallProduct(app, PACKAGENAME)
        

SOCIALPUBLISHER_FIXTURE = CollectiveSocialpublisher()
INTEGRATION_TESTING = \
    IntegrationTesting(bases=(SOCIALPUBLISHER_FIXTURE, ),
                       name="CollectiveSocialpublisher:Integration")
FUNCTIONAL_TESTING = \
    FunctionalTesting(bases=(SOCIALPUBLISHER_FIXTURE, ),
                       name="CollectiveSocialpublisher:Functional")
