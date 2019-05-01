from lib.page import Page
from pathlib import Path
import json
from glob import glob
#list of pages 
pages=[]

def generatePages():
	for pageJson in Path('./app/pages').glob('**/*'):
		#get json data of page
		pages.append(Page(data=pageJson.name))
		