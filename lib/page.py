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

#**static asserts for pages(e.g: css/style.css or img/myImg.png)
#dict of path-url pairs(e.g.  path:css/style.css - url:css/style)
staticAsserts=[]


class Page:
	def __init__(self, data):
		if not data:
			raise ValueError('data is required')
		else:
			self.dataPath=Path('./app/pages/'+data)
	
	def servePage(self):		
		if self.data['auth']:
			@auth_basic(check)
			def serve():
				if self.data['debug']:
					self.render()
				return static_file(Path(self.data['path']).name, root="static/")
		else:
			def serve():
				if self.data['debug']:
					self.render()
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
			if self.data['debug']:
				outputCss=''
				for cssPath in self.data['css']:
					cssUrl='/css/'+cssPath
					outputCss+='<link href="'+cssUrl+'" rel="stylesheet" type="text/css">'
					if cssUrl not in staticAsserts:
						staticAsserts.append(cssUrl)
						
				tempData.update({"css":outputCss})
			else:
				outputCss=''
				for cssPath in self.data['css']:
					outputCss+='<style>'+cssmin(Path('./app/css/'+cssPath).read_text())+'</style>'
				tempData.update({"css":outputCss})
		
		#**prepare js
		if 'js' in self.data and len(self.data['js']):
			if self.data['debug']:
				outputJs=''
				for jsPath in self.data['js']:
					jsUrl='/js/'+jsPath
					outputJs+='<script src="'+jsUrl+'"></script>'
					if jsUrl not in staticAsserts:
							staticAsserts.append(jsUrl)
				
				tempData.update({"js":outputJs})
			else:
				outputJs=''
				for jsPath in self.data['js']:
					outputJs+='<script>'+jsmin(Path('./app/js/'+jsPath).read_text())+'</script>'
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
		if self.data['debug']:
			for src in srcList:
				imgFileUrl='/img/'+src
				staticAsserts.append(imgFileUrl)
		else:
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
		