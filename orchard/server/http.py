from server import *
from ConcurrenTree.util.server import httpfileserver
import os.path

import ConcurrenTree

class HTTP(PoolServer):
	def __init__(self, port=8080):
		self.closed = False
		self.port = port
		self.rootpath = ConcurrenTree.__path__[0]
		print "HTTP server root path:",self.rootpath
		def jsclient(path):
			return os.path.join(self.rootpath,"orchard/jsclient/", path)
		def img(path):
			return os.path.join(self.rootpath,"img/", path)
		self.server = httpfileserver.Server(('',port), {
			'/':(jsclient("client.html"),'text/html'),
			'/index.htm':(jsclient("client.html"),'text/html'),
			'/index.html':(jsclient("client.html"),'text/html'),
			'/newclient':(jsclient("newclient.html"),'text/html'),
			'/util.js':(jsclient("util.js"),'text/javascript'),
			'/buffer.js':(jsclient("buffer.js"),'text/javascript'),
			'/ctree.js':(jsclient("ctree.js"),'text/javascript'),
			'/operation.js':(jsclient("operation.js"),'text/javascript'),
			'/bcp.js':(jsclient("bcp.js"),'text/javascript'),
			'/view.js':(jsclient("view.js"),'text/javascript'),
			'/stream.js':(jsclient("stream.js"),'text/javascript'),
			'/jquery.js':(jsclient("jquery-1.4.2.min.js"),'text/javascript'),
			'/jquery-1.4.2.min.js':(jsclient("jquery-1.4.2.min.js"),'text/javascript'),
			'/textile.js':(jsclient("textile-editor.min.js"),'text/javascript'),
			'/textile-editor.min.js':(jsclient("textile-editor.min.js"),'text/javascript'),
			'/head.js':(jsclient("head.min.js"),'text/javascript'),
			'/img/logo.svg':(img("logos/OrchardLogo.svg"),'image/svg+xml'),
			'/OrchardLogo.svg':(img("logos/OrchardLogo.svg"),'image/svg+xml'),
			'/img/biglogo.svg':(img("logos/OrchardBigLogo.svg"),'image/svg+xml'),
			'/OrchardBigLogo.svg':(img("logos/OrchardBigLogo.svg"),'image/svg+xml'),
			'/favicon.ico':(img("logos/Orchard32.ico"),'image/svg+xml') #find mime type for ico
		})
		self._policy = Policy()

	def run(self):
		startmessage('HTTP',self.port)
		self.server.start()

	def starting(self):
		return []

	def policy(self):
		return self._policy

	def close(self):
		self.server.closed = True
		self.server.close()

