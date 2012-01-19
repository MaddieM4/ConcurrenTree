from ConcurrenTree.util.server import http

import ConcurrenTree

import webbrowser

class HTTP(http.HTTPServer):
	def __init__(self, auth, port=8080, **options):
		http.HTTPServer.__init__(self, port=port, **options)

		jsclient = ConcurrenTree.file("orchard/jsclient/")
		js = ConcurrenTree.file("orchard/jsclient/js")
		css = ConcurrenTree.file("orchard/jsclient/css")
		img = ConcurrenTree.file("img/logos")

		http.Alias(self, "/favicon.ico", "Orchard32.ico", img)
		http.Alias(self, "/", "index.html", jsclient)
		http.Alias(self, "/index", "index.html", jsclient)

		http.FileServer(self, "tab", jsclient+"tab/")
		http.FileServer(self, "js", js)
		http.FileServer(self, "css", css)
		http.FileServer(self, "bootstrap", jsclient+"bootstrap/", False)
		http.FileServer(self, "img", img)

		http.Alias(self, "/js/head.js", "head.min.js", js)
		http.Alias(self, "/js/jquery.js", "jquery-1.4.2.min.js", js)
		http.Alias(self, "/js/textile.js", "textile-editor.min.js", js)
		http.Alias(self, "/js/stream/ws.js", "ws.js", js)

		http.Callback(self, "/account/new", self.newAccount, method="POST")
		http.Callback(self, "/account/form", self.newAccountForm)

		self.rootpath = jsclient
		self.port = port
		self.auth = auth

	def newAccount(self, request):
		d = dict(request.forms)
		if 'username' in d and 'password' in d:
			self.auth.new(d['username'], d['password'])
			return ["Created successfully!"]
		return ["Missing username or password arguments."]

	def newAccountForm(self, request):
		return [
			"<html><head><title>Make a new account</title></head>",
			"<body><form method='POST' action='/account/new'>",
			"Username: <input type='text' name='username'><br/>",
			"Password: <input type='password' name='password'><br/>",
			"<input type='submit'>",
			"</form></body></html>"
		]

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
