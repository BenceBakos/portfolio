"""
data
	css
	js
	template
	content
	path
	url
render()
"""
from pathlib import Path
from cssmin import cssmin
from jsmin import jsmin
from bottle import SimpleTemplate,static_file,auth_basic
from lib.auth import check
import json
import re
import base64

#***RELOADER***
#true mean, rerender on every call
reloader=True

class Page:
	def __init__(self, data):
		if not data:
			raise ValueError('data is required')
		else:
			self.dataPath=Path('./app/pages/'+data)
	
	def servePage(self):
		global reloader
		
		
		
		if self.data['auth']:
			@auth_basic(check)
			def serve():
				if reloader:
					self.render()
					print(self.data['path']+' is reoaded')
				return static_file(Path(self.data['path']).name, root="static/")
		else:
			def serve():
				if reloader:
					self.render()
					print(self.data['path']+' is reoaded')
				return static_file(Path(self.data['path']).name, root="static/")
		
		return serve()
	
	def render(self):
		self.data=json.loads(self.dataPath.read_text())
		tempData={}
		#**auth**
		if 'auth' not in self.data:
			self.data['auth']=False
		
		#**prepare css
		if 'css' in self.data and len(self.data['css']):
			outputCss=''
			for cssPath in self.data['css']:
				outputCss+=cssmin(Path('./app/css/'+cssPath).read_text())
			tempData.update({"css":outputCss})
		
		#**prepare js
		if 'js' in self.data and len(self.data['js']):
			outputJs=''
			for jsPath in self.data['js']:
				outputJs+=jsmin(Path('./app/js/'+jsPath).read_text())
			tempData.update({"js":outputJs})
		
		
		#**prepare content
		outputContent={}
		if 'content' in self.data and self.data['content']:
			for contKey, contPath in self.data['content'].items():
				contentFile=Path('./app/content/'+contPath)
				if contentFile.is_file():
					outputContent[contKey]=contentFile.read_text()
				else:
					outputContent[contKey]=" "
					contentFile.write_text(" ")
			tempData.update(outputContent)
		else:
			tempData['content']=''
		
		#**create document
		documentTmp=SimpleTemplate(Path('./app/template/'+self.data['template']).read_text())
		document=documentTmp.render(tempData)
		
		#***replace images with base64***
		srcList=re.findall('<img[^>]+src="([^">]+)"', document)
		for src in srcList:
			imgFile=Path('./app/img/'+src)
			if imgFile.is_file():
				imgBase64=base64.b64encode(open(imgFile.as_posix(), 'rb').read()).decode('utf-8').replace('\n', '')
				document=document.replace(src,'data:image/'+src.split('.')[1]+';charset=utf-8;base64, {0}'.format(imgBase64))
		
		#**write document to file
		documentPath=Path('./static/'+self.data['path'])
		documentPath.write_text(document)
		
		#**save path
		self.path=documentPath
		