from lib.page import Page
from pathlib import Path
import json
from glob import glob
#list of pages 
pages=[]

def generatePages():
	for pageJson in Path('./app/pages').glob('**/*'):
		#get json data of controller
		pageData=json.loads(pageJson.read_text())
		pages.append(Page(data=pageData))
		