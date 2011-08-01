from server import *
from ConcurrenTree.util.server import httpfileserver as hfs
import os.path

import ConcurrenTree

class HTTP(PoolServer):
	def __init__(self, port=8080):
		self.closed = False
		self.port = port
		self.rootpath = ConcurrenTree.__path__[0]
		print "HTTP server root path:",self.rootpath

		jsclient = os.path.join(self.rootpath,"orchard/jsclient/")
		img = os.path.join(self.rootpath,"img/")

		self.server = hfs.Server(('',port), [
			hfs.File(jsclient,"client.html",["/","/index.htm","/index.html"],'text/html'),
			hfs.File(jsclient,"newclient.html", "/newclient", "text/html"),
			hfs.File(jsclient,"util.js", mimetype="text/javascript"),
			hfs.File(jsclient,"buffer.js", mimetype="text/javascript"),
			hfs.File(jsclient,"ctree.js", mimetype="text/javascript", preload=True),
			hfs.File(jsclient,"operation.js", mimetype="text/javascript"),
			hfs.File(jsclient,"bcp.js", mimetype="text/javascript", preload=True),
			hfs.File(jsclient,"view.js", mimetype="text/javascript", preload=True),
			hfs.File(jsclient,"stream.js", mimetype="text/javascript"),
			hfs.File(jsclient,"jquery-1.4.2.min.js", ["/jquery.js", "/jquery-1.4.2.min.js"],"text/javascript", browsercache=True, cache=True, preload=True),
			hfs.File(jsclient,"textile-editor.min.js", ["/textile.js", "/textile-editor.js"],"text/javascript"),
			hfs.File(jsclient,"head.min.js", "/head.js", mimetype="text/javascript", browsercache=True, cache=True, preload=True),
			hfs.File(img,"logos/OrchardLogo.svg", ["/img/logo.svg", "/OrchardLogo.svg"],"image/svg+xml", browsercache=True),
			hfs.File(img,"logos/OrchardBigLogo.svg", ["/img/biglogo.svg", "/OrchardBigLogo.svg"],"image/svg+xml", browsercache=True),
			hfs.File(img,"logos/Orchard32.ico", "/favicon.ico","image", browsercache=True)
		])
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

