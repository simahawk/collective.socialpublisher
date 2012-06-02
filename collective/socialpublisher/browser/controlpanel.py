# from z3c.form import form, button

from plone.app.registry.browser.controlpanel import RegistryEditForm
# from plone.app.registry.browser.controlpanel import _ as registryMF

from collective.socialpublisher.interfaces import IGlobalSettings
from collective.socialpublisher import _


class ControlPanelForm(RegistryEditForm):
    schema = IGlobalSettings
    label = _("Social publisher global settings")

    def applyChanges(self, data):
        super(ControlPanelForm, self).applyChanges(data)
        pass
