#***ASYNC***
from gevent import monkey; monkey.patch_all()
#***SERVER***
from bottle import Bottle, static_file
app = Bottle()

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
		app.route(page.data['url'],['get'],page.servePage)		


#***SERVE STATIC FOLDER***
"""@app.route("/<filepath:path>",["get"])
def static(filepath):
	print(filepath)
	return static_file(filepath, root="./static/")
"""
#***CMS***
import lib.cms as cms
#serve cms page
@app.route("/admin",['get'],cms.serveCmsPage)
#update content
@app.route("/admin/update",['post'],cms.update)
@app.route("/admin/contents",['get'],cms.getContents)


#***ROUTES***

@app.route('/asd')
def asd():
	return "asd"

#***RUN SERVER***
app.run(host='localhost', port=3000, server='gevent', debug=True,reloader=True)