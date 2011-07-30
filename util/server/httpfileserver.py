from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class BaseFileHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		files = self.files().dict
		try:
			#print self.path
			#print files[self.path]
			self.path = self.path.split("?")[0]
			ctype = path = None

			if type(files[self.path])==tuple:
				path, ctype = files[self.path]
			else:
				path, ctype = (files[self.path],'text/plain')

			with open(path) as f:
				self.send_response(200)
				self.send_header('Content-type',ctype)
				self.end_headers()
				self.wfile.write(f.read())
				return
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

class Server:
	def __init__(self, address=('',80), files={}):
		self.files = dict_by_reference(files)
		self.handler = make_handler(self.files)
		self.server = HTTPServer(address, self.handler)

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
