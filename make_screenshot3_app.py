from lxml import etree
from pyppeteer import launch
from sanic import response
from sanic.response import file_stream
import asyncio
import gzip
import os
import sanic
import urllib.request
from urllib.parse import unquote
#import urllib
import zipfile
import shutil
from pyppeteer.errors import PageError
   
app = sanic.Sanic()

async def root_func(request):
   return sanic.response.json({'resp': request})

async def screenshots_func(request, uid):
   my_url = "http://{0}/sitemap.xml.gz".format(uid)
   sitemap = urllib.request.urlopen(my_url)
   sitemap_data = gzip.decompress(sitemap.read())
   parser = etree.XMLParser(remove_blank_text=True)
   elem = etree.XML(sitemap_data, parser=parser)
   folder_id = newString = "".join(uid.split("."))
   if not os.path.exists(folder_id):
       #maybe python3 mkdir-temporary.py
       os.mkdir(folder_id)
   
   no_screensthots = await screenshot_do(elem, folder_id)
   return_text = 'rendering {0} screensthots in folder {1} - come back later'.format(no_screensthots, folder_id)
   return response.text("http://localhost:5006/get_files/{0}".format(folder_id))
   
 
async def screenshot_do(elem, folder_id):
   shots = 0
   screenshots = []
   for element in elem:
       webpage = element[0].text
       pagename = webpage.replace("http://", "")
       pagename = pagename.replace(".", "-")
       pagename = pagename.replace("/", "-") + '.png'
       shots += 1
       screenshots.append(pagename)
       pathname = '{0}/{1}'.format(folder_id, pagename)
       exists = os.path.isfile(pathname)
       if exists:
           nothin = 0
           #print('done before: {0}'.format(pagename))
       else:
           # make preview with pyppeteer
           browser = await launch()
           page = await browser.newPage()
           await page.setViewport({'width': 1700, 'height': 2400})
           await page.goto(webpage)
           height = await page.evaluate("() => document.body.scrollHeight")
           await page.setViewport({'width': 2400, 'height': height})
           await page.screenshot({'path': pathname})
           await browser.close()
           #print('saved screenshot: {0}'.format(pagename))
   return shots

async def make_screenshot_func(request, uid):
   # make preview with pyppeteer
   adr = unquote(uid)
   plone_page =  adr
   #plone_page = 'http://medialog.no'
   browser = await launch()
   page = await browser.newPage()
   await page.setViewport({'width': 1700, 'height': 3000})
   await page.goto(plone_page)
   height = await page.evaluate("() => document.body.scrollHeight")
   await page.setViewport({'width': 1700, 'height': height})
   await asyncio.sleep(5)
   await page.screenshot({'path': 'screenshot.png'})
   await browser.close()
   return await response.file('screenshot.png')

def get_files_func(request, uid):
   output_filename = uid
   folder_id = uid
   shutil.make_archive(output_filename, 'gztar', folder_id)
   return response.file('{0}.tar.gz'.format(output_filename))
   
app.add_route(make_screenshot_func, '/make_screenshot/<uid>', methods=['GET'])
app.add_route(get_files_func, '/get_files/<uid>', methods=['GET'])
app.add_route(screenshots_func, '/screenshots/<uid>', methods=['GET'])
if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5007, workers=2)