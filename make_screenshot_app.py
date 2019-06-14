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


async def sitemap(request, path):
   #maybe add check for sitemap.xml
   sitemap = urllib.request.urlopen(path)
   sitemap_data = gzip.decompress(sitemap.read())
   parser = etree.XMLParser(remove_blank_text=True)
   elem = etree.XML(sitemap_data, parser=parser)
   folder_id = newString = "".join(uid.split("."))
   if not os.path.exists(folder_id):
       #maybe python3 mkdir-temporary.py
       os.mkdir(folder_id)

   no_screensthots = await screenshot_do(elem, folder_id)
   return_text = 'rendering {0} screensthots in folder {1} - come back later'.format(no_screensthots, folder_id)
   return response.text("http://localhost:5000/get_files/{0}".format(folder_id))


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
           try:
               browser = await launch()
               page = await browser.newPage()
               await page.setViewport({'width': 1700, 'height': 3000})
               await page.goto(webpage)
               height = await page.evaluate("() => document.body.scrollHeight")
               await page.setViewport({'width': 2400, 'height': height})
               #await asyncio.sleep(3)
               await page.screenshot({'path': pathname})
               await browser.close()
               #print('saved screenshot: {0}'.format(pagename))
           except Exception:
              continue
           except PageError:
              print('skipping link')
              continue
   return shots


# async def plone_screenshot(request, path):
#    # make preview with pyppeteer
#    pagename = path.replace("http://", "")
#    pagename = path.replace(".", "-")
#    pagename = path.replace("/", "-") + '.png'
#    try:
#        browser = await launch()
#        page = await browser.newPage()
#        await page.setViewport({'width': 1700, 'height': 3000})
#        await page.goto(path)
#        height = await page.evaluate("() => document.body.scrollHeight")
#        await page.setViewport({'width': 1700, 'height': height})
#        #await asyncio.sleep(3)
#        await page.screenshot({'path': pagename})
#        await browser.close()
#        #return await response.file(pagename)
#        return await response.text(pagename)
#    except Exception:
#        continue
#    except PageError:
#        print('skipping link')
#        continue


async def screenshot(request, path):
   # make preview with pyppeteer
   try:
       browser = await launch()
       page = await browser.newPage()
       await page.setViewport({'width': 1700, 'height': 3000})
       await page.goto(path)
       height = await page.evaluate("() => document.body.scrollHeight")
       await page.setViewport({'width': 1700, 'height': height})
       #await asyncio.sleep(3)
       await page.screenshot({'path': 'screenshot.png'})
       await browser.close()
       return await response.file('screenshot.png')

   except Exception:
       pass

   except PageError:
       print('skipping link')
       pass

def get_files(request, name):
    output_filename = name
    folder_id = name
    shutil.make_archive(output_filename, 'gztar', folder_id)
    return response.file('{0}.tar.gz'.format(output_filename))

app.add_route(sitemap, '/sitemap/<mypath:path>')
app.add_route(get_files, '/get_files/<name>')
app.add_route(screenshot, '/screenshot/<mypath:path>')

if __name__ == "__main__":
   app.run(host="0.0.0.0", port=5000, workers=2)
