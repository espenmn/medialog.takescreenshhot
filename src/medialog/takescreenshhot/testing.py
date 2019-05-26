# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import applyProfile
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneSandboxLayer
from plone.testing import z2

import medialog.takescreenshhot


class MedialogTakescreenshhotLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=medialog.takescreenshhot)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'medialog.takescreenshhot:default')


MEDIALOG_TAKESCREENSHHOT_FIXTURE = MedialogTakescreenshhotLayer()


MEDIALOG_TAKESCREENSHHOT_INTEGRATION_TESTING = IntegrationTesting(
    bases=(MEDIALOG_TAKESCREENSHHOT_FIXTURE,),
    name='MedialogTakescreenshhotLayer:IntegrationTesting',
)


MEDIALOG_TAKESCREENSHHOT_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(MEDIALOG_TAKESCREENSHHOT_FIXTURE,),
    name='MedialogTakescreenshhotLayer:FunctionalTesting',
)


MEDIALOG_TAKESCREENSHHOT_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        MEDIALOG_TAKESCREENSHHOT_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='MedialogTakescreenshhotLayer:AcceptanceTesting',
)
