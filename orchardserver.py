''' 
Wrappers that subclass BCP.PoolServer. This lets us run
our servers with the BCP.ServerPool framework.

There's a lot of useful and fairly general code in here,
so as always, feel free to copy it out for your own 
non-Orchard use.

'''

import httpfileserver
import os.path

from BCP.serverpool import PoolServer

class HTTP(PoolServer):
	def __init__(self, port=8080):
		def derel(path):
			return os.path.join(os.path.curdir,"./jsclient/", path)
		self.server = httpfileserver.Server(('',port), {
			'/':(derel("client.html"),'text/html'),
			'/index.htm':(derel("client.html"),'text/html'),
			'/index.html':(derel("client.html"),'text/html'),
			'/chainer.js':(derel("chainer.js"),'text/javascript'),
			'/ctree.js':(derel("ctree.js"),'text/javascript'),
			'/operation.js':(derel("operation.js"),'text/javascript'),
			'/jquery.js':(derel("jquery-1.4.2.min.js"),'text/javascript'),
			'/jquery-1.4.2.min.js':(derel("jquery-1.4.2.min.js"),'text/javascript'),
			'/textile-editor.min.js':(derel("textile-editor.min.js"),'text/javascript'),
			'/img/logo.svg':(derel("OrchardLogo.svg"),'image/svg+xml'),
			'/OrchardLogo.svg':(derel("OrchardLogo.svg"),'image/svg+xml'),
			'/img/biglogo.svg':(derel("OrchardBigLogo.svg"),'image/svg+xml'),
			'/OrchardBigLogo.svg':(derel("OrchardBigLogo.svg"),'image/svg+xml')
		})

	def run(self):
		self.server.start()

	def starting(self):
		return []

	def close(self):
		self.server.close()

class WebSocket(PoolServer):
	pass

class Peers(PoolServer):
	pass

class HALP(PoolServer):
	pass

class DHT(PoolServer):
	''' By default, the Kademlia CTree hosting cloud. '''
	pass
