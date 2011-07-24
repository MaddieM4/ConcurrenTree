from BCP.serverpool import PoolServer, Policy
import orchardserver

import httpfileserver
import os.path

class HTTP(PoolServer):
	def __init__(self, port=8080):
		self.closed = False
		self.port = port
		def derel(path):
			return os.path.join(os.path.curdir,"./jsclient/", path)
		self.server = httpfileserver.Server(('',port), {
			'/':(derel("client.html"),'text/html'),
			'/index.htm':(derel("client.html"),'text/html'),
			'/index.html':(derel("client.html"),'text/html'),
			'/newclient':(derel("newclient.html"),'text/html'),
			'/util.js':(derel("util.js"),'text/javascript'),
			'/buffer.js':(derel("buffer.js"),'text/javascript'),
			'/ctree.js':(derel("ctree.js"),'text/javascript'),
			'/operation.js':(derel("operation.js"),'text/javascript'),
			'/bcp.js':(derel("bcp.js"),'text/javascript'),
			'/view.js':(derel("view.js"),'text/javascript'),
			'/stream.js':(derel("stream.js"),'text/javascript'),
			'/jquery.js':(derel("jquery-1.4.2.min.js"),'text/javascript'),
			'/jquery-1.4.2.min.js':(derel("jquery-1.4.2.min.js"),'text/javascript'),
			'/textile.js':(derel("textile-editor.min.js"),'text/javascript'),
			'/textile-editor.min.js':(derel("textile-editor.min.js"),'text/javascript'),
			'/head.js':(derel("head.min.js"),'text/javascript'),
			'/img/logo.svg':(derel("OrchardLogo.svg"),'image/svg+xml'),
			'/OrchardLogo.svg':(derel("OrchardLogo.svg"),'image/svg+xml'),
			'/img/biglogo.svg':(derel("OrchardBigLogo.svg"),'image/svg+xml'),
			'/OrchardBigLogo.svg':(derel("OrchardBigLogo.svg"),'image/svg+xml'),
			'/favicon.ico':(derel("../img/logos/Orchard32.ico"),'image/svg+xml') #find mime type for ico
		})
		self._policy = Policy()

	def run(self):
		orchardserver.startmessage('HTTP',self.port)
		self.server.start()

	def starting(self):
		return []

	def policy(self):
		return self._policy

	def close(self):
		self.server.closed = True
		self.server.close()

