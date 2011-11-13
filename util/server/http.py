import bottle
from bottle import static_file
from pool.server import Server
from pool.policy import Policy

bottle.debug()

class HTTPServer(Server):
	def __init__(self, host="localhost", port=8080):
		self.host = host
		self.port = port
		self._policy = Policy()
		self.server = bottle.Bottle()
		self.wsgi = None
		self.closed = False
		self.mounts = set()

	def run(self):
		bottle.run(self.server, server=KillableWSGIRefServer, host=self.host, port=self.port, setserver=self.setserver)

	def starting(self):
		return []

	def policy(self):
		return self._policy

	def close(self):
		print "Shutting down HTTP server..."
		self.closed = True
		self.server.close()
		self.wsgi.shutdown()
		print "HTTP server shut down."

	def new(self):
		''' Returns a Bottle object so other modules don't have to import bottle '''
		return bottle.Bottle()

	def route(self, path="/", **options):
		return self.server.route(path=path, **options)

	def mount(self, prefix, server, **options):
		''' Mounts a WSGI server (such as a Bottle) to a prefix on this server '''
		if not server in self:
			self.server.mount(server, prefix, **options)
			self.mounts.add((prefix, server, freeze_dict(options)))

	def unmount(self, server):
		''' Unmounts a previously mounted WSGI server '''
		if server in self:
			self.mounts.remove(self[server])
			self.reset()
			self.remount()

	def remount(self):
		''' Mount every element of self.mounts to internal server '''
		for i in self.mounts:
			self.mount(i[0], i[1], **thaw_dict(i[2]))

	def reset(self):
		''' Unmount everything from internal server. Doesn't affect self.mounts '''
		self.server.reset()

	def setserver(self, wsgi):
		self.wsgi = wsgi

	@property
	def properties(self):
		return {
			"mounts":list(self.mounts),
			"port":self.port,
			"hostname":self.hostname
		}

	def __contains__(self, obj):
		for i in self.mounts:
			if i[1] == obj:
				return True

	def __getitem__(self, obj):
		for i in self.mounts:
			if i[1] == obj:
				return i

def FileServer(bserver, prefix, ospath, onelayer=True):
	''' Use onelayer to restrict path pattern matching to one folder of heirarchy '''
	if not prefix.endswith("/"):
		prefix += "/"
	if not prefix.startswith("/"):
		prefix = "/" + prefix
	if onelayer:
		prefix += ":name"
	else:
		prefix += ':name#.*#'

	def printandserve(name):
		print "Attempting to serve ",repr(name)," from ",repr(ospath)
		return static_file(name, ospath)

	return bserver.route(prefix)(printandserve)

class KillableWSGIRefServer(bottle.WSGIRefServer):
	def run(self, handler):
		''' Copied and pasted from Bottle source, unfortunately. I hate the hackiness of that. '''

		from wsgiref.simple_server import make_server, WSGIRequestHandler
		if self.quiet:
			class QuietHandler(WSGIRequestHandler):
				def log_request(*args, **kw): pass
			self.options['handler_class'] = QuietHandler

		setserver = self.options['setserver']
		del self.options['setserver']

		srv = make_server(self.host, self.port, handler, **self.options)
		setserver(srv)
		srv.serve_forever()

def Alias(bserver, route, filename, ospath):
	return bserver.route(route)(lambda:static_file(filename, ospath))

def freeze_dict(d):
	''' No shrinkage jokes please. '''
	return frozenset(d.iteritems())

def thaw_dict(d):
	result = {}
	for key, value in d:
		result[key] = value
	return result
