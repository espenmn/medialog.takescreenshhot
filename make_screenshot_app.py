#import urllib
from lxml import etree
from pyppeteer import launch
from pyppeteer.errors import PageError
from sanic import response
from sanic.response import file_stream
from urllib.parse import unquote
import asyncio
import gzip
import os
import random
import sanic
from sanic.response import json
import shutil
import urllib.request
import zipfile
import pdb

app = sanic.Sanic()
#app.config.RESPONSE_TIMEOUT = 1000


@app.route('/single_screenshot/<folder_name:string>/<image_name:string>/<mypath:path>', methods=['POST'])
async def single_screenshot(request, folder_name, image_name, mypath):
    #make a folder to save the images in
    if not os.path.exists(folder_name):
        os.mkdir(folder_name)

    path_name="{0}/{1}.png".format(folder_name, image_name)
    browser = await launch()
    page = await browser.newPage()
    await page.setViewport({'width': 1700, 'height': 3000})
    await page.goto(mypath)
    height = await page.evaluate("() => document.body.scrollHeight")
    await page.setViewport({'width': 1700, 'height': height})
    #wait for lazy loading images
    await asyncio.sleep(3)
    await page.screenshot({'path': path_name})
    await browser.close()
    return response.text(path_name)


# @app.route('/screenshots', methods=['POST'])
# async def single_screenshot(request, *args):
#     #make a folder to save the images in
#
#     arg = request.args
#     print(args)
#     folder_name = 'somefolder'
#     image_name = 'somtimage'
#     if not os.path.exists(folder_name):
#         os.mkdir(folder_name)
#
#     path_name="{0}/{1}.png".format(folder_name, image_name)
#     print(path_name)
#     browser = await launch()
#     page = await browser.newPage()
#     await page.setViewport({'width': 1700, 'height': 3000})
#     await page.goto(mypath)
#     height = await page.evaluate("() => document.body.scrollHeight")
#     await page.setViewport({'width': 1700, 'height': height})
#     #wait for lazy loading images
#     await asyncio.sleep(3)
#     await page.screenshot({'path': path_name})
#     await browser.close()
#     return response.text(path_name)


if __name__ == "__main__":
  app.run(host="0.0.0.0", port=5010, workers=2)
