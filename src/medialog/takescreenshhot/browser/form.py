#import urllib.request
import requests
import gzip
from plone import api
from plone.supermodel import model
from Products.Five import BrowserView
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import button
from zope import schema
from zope.interface import alsoProvides

from zope.i18nmessageid import MessageFactory

_ = MessageFactory('medialog.takescreenshhot')

class ScreenshotForm(BrowserView):
    """ Define Form handling"""

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        import pdb; pdb.set_trace()
        context = self.context
        page = self.context.absolute_url()
        my_url = "http://localhost:5000/screenshot/{0}".format(page)
        #return requests.get(my_url)
        context.REQUEST.RESPONSE.redirect(my_url)
        #esponse.redirect(my_url, lock=True)
        #response =  requests.get(my_url)
        #return response.text

    #@button.buttonAndHandler(_('Save'), name='save')
    #def handleAdd(self, action):
    #    return 'ost'
