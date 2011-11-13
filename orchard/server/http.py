from ConcurrenTree.util.server import http

import ConcurrenTree

import webbrowser

class HTTP(http.HTTPServer):
	def __init__(self, port=8080, **options):
		http.HTTPServer.__init__(self, port=port, **options)

		jsclient = ConcurrenTree.file("orchard/jsclient/")
		js = ConcurrenTree.file("orchard/jsclient/js")
		css = ConcurrenTree.file("orchard/jsclient/css")
		img = ConcurrenTree.file("img/logos")

		http.Alias(self, "/", "newclient.html", jsclient)
		http.Alias(self, "/newclient", "newclient.html", jsclient)
		http.Alias(self, "/facelift", "facelift.html", jsclient)

		http.FileServer(self, "js", js)
		http.FileServer(self, "css", css)
		http.FileServer(self, "bootstrap", jsclient+"bootstrap/", False)
		http.FileServer(self, "img", img)

		http.Alias(self, "/js/head.js", "head.min.js", js)
		http.Alias(self, "/js/jquery.js", "jquery-1.4.2.min.js", js)
		http.Alias(self, "/js/textile.js", "textile-editor.min.js", js)
		http.Alias(self, "/js/stream/ws.js", "ws.js", js)

		self.rootpath = jsclient
		self.port = port

	def open(self, location="/"):
		''' Open a new browser window '''
		webbrowser.open(self.domain+location)

	@property
	def domain(self):
		return "http://localhost:%d" % self.port

	@property
	def properties(self):
		return {
			"name":"HTTP",
			"closed":self.closed,
			"port":self.port,
			"path":self.rootpath,
			"domain":self.domain,
			"open":self.open,
			"internal_server":self.server
		}
