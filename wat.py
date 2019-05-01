#***SERVER***
import bottle
from bottle import static_file,auth_basic
from lib.auth import check
from pathlib import Path
import json

#***ROUTES FROM JSON***
import lib.page
#(/app/routes)
import lib.pagesFromJson as pagesFromJson
#generate page html files to /static folder
pagesFromJson.generatePages()

#append PAGES to APP as ROUTES based on page.data['url']
for page in pagesFromJson.pages:
	#render page
	page.render()
	#create route
	if page.data['url']:
		if page.data['auth']:
			
			bottle.route(page.data['url'],['get'],page.servePage)		
		else:
			bottle.route(page.data['url'],['get'],page.servePage)		


#***SERVE STATIC FOLDER***
"""bottle.route("/<filepath:path>",["get"])
def static(filepath):
	print(filepath)
	return static_file(filepath, root="./static/")
"""
#***CMS***
import lib.cms as cms
#update content
bottle.route("/admin/update",['post'],cms.update)
bottle.route("/admin/contents",['get'],cms.getContents)


#***ROUTES***

"""bottle.route('/asd')
def asd():
	return "asd"
"""

#***RUN SERVER***
#DEPLOY:next line is unneccessary on wsgi server.
bottle.run(host='localhost', port=3000, debug=True,reloader=True)


"""
wsgi config file:
# This file contains the WSGI configuration required to serve up your
# web application at http://<your-username>.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.
#
# The below has been auto-generated for your Bottle project
import os
import sys

# add your project directory to the sys.path
project_home = u'/home/bakben/portfolio'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# make sure the default templates directory is known to Bottle
#templates_dir = os.path.join(project_home, 'views/')
#if templates_dir not in bottle.TEMPLATE_PATH:
#    bottle.TEMPLATE_PATH.insert(0, templates_dir)

# import bottle application
#***ASYNC***

import bottle
import wat
application = bottle.default_app()


"""