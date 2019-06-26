#import urllib.request
import re
import requests
import gzip
from plone import api
from plone.supermodel import model
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.statusmessages.interfaces import IStatusMessage
from z3c.form import form
from z3c.form import field
from z3c.form import button
from zope import schema
from zope.interface import alsoProvides

from plone.autoform.form import AutoExtensibleForm

from zope.i18nmessageid import MessageFactory

_ = MessageFactory('medialog.takescreenshhot')




class IScreenshotForm(model.Schema):
     """ Define form fields """

     names = schema.ASCII(
                title=u"URLs",
                description=u"One on each line. For sitemap: Only base URL ( http://medialog.no )",
                required=False
          )


class ScreenshotForm(AutoExtensibleForm, form.Form):
    """ Make screenshots (png)"""

    schema = IScreenshotForm
    #template = ViewPageTemplateFile("screentshot.pt")
    ignoreContext = True
    success = False

    @button.buttonAndHandler(u'This page')
    def handleApply(self, action):
        #send url to (make) single screenshot
        url = self.context.absolute_url()
        return self.single_screensthot(url)

    @button.buttonAndHandler(u'Sub content')
    def handleApply(self, action):
        context=self.context
        #all content below here
        #consider using 'depth' to limit
        kontents = api.content.find(context)
        for kontent in kontents:
            url = kontent.getObject().absolute_url()
            #print url
            self.single_screensthot(url)
            IStatusMessage(self.request).addStatusMessage(url, "info")

    @button.buttonAndHandler(u'URL list')
    def handleApply(self, action):
        #make screenshots of (text)list of urls
        my_data = self.extractData()
        if my_data:
            shots = []
            folder = 'screenshots'
            pages = my_data[0]['names']
            urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', pages)
            if urls:
                for url in urls:
                    name = self.single_screensthot(url)
                    IStatusMessage(self.request).addStatusMessage(name, "info")
        IStatusMessage(self.request).addStatusMessage('Please check your input', "warning")

    @button.buttonAndHandler(u'Sitemap')
    def handleApply(self, action):
         #make screenshots of all in Plone sitemap
         my_data = self.extractData()
         if my_data:
             pages = my_data[0]['names']
             urls = re.findall('https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', pages)
             if urls:
                 for url in urls:
                     my_url = "http://localhost:5010/sitemap/%s" % url
                     response = requests.post(my_url)
                     image_path = "One day, maybe avalable at http://localhost:5010/get_files/%s " % response.text
                     IStatusMessage(self.request).addStatusMessage(
                        image_path, "info"
                     )
         IStatusMessage(self.request).addStatusMessage(
                'Please check your input', "warning"
         )

    def make_screensthot(self, my_urls, folder_name):
         pages = []
         for my_url in my_urls:
              page = my_url.getObject().absolute_url()
              page_name = my_url.getObject().title
              my_url = "http://localhost:5010/single_screenshot/%s/%s/%s" % (folder_name, page_name, page)
              response = requests.post(my_url)
              pages.append(response.text)
         return pages

    def single_screensthot(self, page):
         folder_name = 'screenshots'
         page_name = page.replace("http://", "")
         page_name = page_name.replace("https/::", "-")
         page_name = page_name.replace(".", "-")
         page_name = page_name.replace(":", "-")
         page_name = page_name.replace("/", "-")
         my_url = "http://localhost:5010/single_screenshot/%s/%s/%s" % (folder_name, page_name, page)
         response = requests.post(my_url)
         image_path = "Image soon avalable at http://localhost:5010/get_file/%s " % page_name
         IStatusMessage(self.request).addStatusMessage(
                    image_path, "info"
         )
         #return response

    #def updateActions(self):
    #    self.actions[u"Sitemap].addClass("black")
