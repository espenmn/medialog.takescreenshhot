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
        context = self.context
        folder_name = self.context.Title()
        my_urls = api.content.find(context=context)
        return self.make_screenshot(folder_name, my_urls)

    def make_screenshot(self, folder_name, my_urls):
        pages_done = []
        #call one and one page until I find out how to do this the right way
        for my_url in my_urls:
            obj = my_url.getObject()
            page = obj.absolute_url().replace(" ", "")
            page_name = obj.Title.replace(" ", "")
            my_url = "http://localhost:5010/single_screenshot/%s/%s/%s" % (folder_name, page_name, page)
            response = requests.post(my_url)
            pages_done.append(response)

        return 1


    # def __call__(self):
    #     context = self.context
    #     my_urls = api.content.find(context=context)
    #     import pdb; pdb.set_trace()
    #     #page = self.context.absolute_url()
    #     my_url = "http://localhost:5010/screenshots"
    #     data = '''{
    #       "query": {
    #             "folder_name": 'my_folder_with_images',
    #             "pages": [['http://medialog.no', 'image1.png'], ['http://plone.org', 'image2.png']
    #         }'''
    #
    #     response = requests.post(my_url, data)
    #     return response
