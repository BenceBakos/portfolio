from pathlib import Path
import json
from bottle import response,request,auth_basic
from lib.auth import check
import os
#get contents path
def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles


#get contents
"""
JSON
[
	path:{
		fileName
		text
	},
...
]
"""
@auth_basic(check)
def getContents():
	contentFiles=getListOfFiles('./app/content')
	contents={}
	
	for file in contentFiles:
		file=Path(file)
		fName=file.resolve().stem
		text=file.read_text()
		path=file.as_posix()
		contents[path]={
			"fileName":fName,
			"text":text
		}
		
	response.content_type = 'application/json'
	return json.dumps(contents)
	
#update api
"""
JSON
path
text
"""
@auth_basic(check)
def update():
	updateData = request.json
	file=Path(updateData['path'])
	if file.is_file():
		file.write_text(updateData['text'])
		response.status=200
	else:
		response.status=404
	
