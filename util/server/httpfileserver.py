from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import os
import time

def farfuture():
	return time.time()+90000000

class BaseFileHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		try:
			self.path = self.path.split("?")[0]
			f = self.files().dict[self.path]

			self.send_response(200)
			self.send_header('Content-type',f.type)
			if f.browsercache:
				self.send_header('Cache-Control',"max-age="+str(farfuture()))
			self.end_headers()
			self.wfile.write(f.value)
		except (IOError, KeyError):
			self.send_error(404, 'File Not Found: '+self.path)

def make_handler(dbr):
	class handler(BaseFileHandler):
		def files(self):
			return dbr
	return handler

class dict_by_reference:
	def __init__(self, dict):
		self.dict = dict

class File:
	def __init__(self, rootpath, endpath, spath=None, mimetype="text/plain", browsercache=False, cache=False, preload=False):
		self.path = os.path.join(rootpath, endpath)
		if spath == None:
			spath = "/"+endpath
		if type(spath)==str:
			spath = [spath]
		self.spath = spath
		self.type = mimetype
		self._value = None
		self.browsercache = browsercache
		self.cache = cache
		self.preload = preload
		self.mtime = 0
		if self.preload:
			self.load()

	def load(self):
		with open(self.path, "r") as f:
			self._value = f.read()
			self.mtime = os.fstat(f.fileno()).st_mtime

	@property
	def value(self):
		if self._value==None or (not self.cache and self.updated):
			self.load()
		return self._value

	@property
	def updated(self):
		return self.fmtime>self.mtime

	@property
	def fmtime(self):
		return os.stat(self.path).st_mtime		

class Server:
	def __init__(self, address=('',80), files=[]):
		self.files = dict_by_reference({})
		for f in files:
			self.host(f)
		self.handler = make_handler(self.files)
		self.server = HTTPServer(address, self.handler)

	def host(self, fileobj):
		for i in fileobj.spath:
			self.files.dict[i] = fileobj

	def start(self):
		self.server.serve_forever()

	def close(self):
		print "Shutting down HTTP server"
		self.server.shutdown()
		print "HTTP server killed"

def main():
	server = Server(('',8080), {"/futurenotes":("/home/philip/documents/ConcurrenTree/futurenotes","text/html")})
	try:
		server.start()
	except KeyboardInterrupt:
		server.close()

if __name__=="__main__":
	main()
