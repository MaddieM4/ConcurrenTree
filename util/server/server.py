class Server(object):
	''' Base class for ServerPool Servers. '''
	def run(self):
		''' Start the server running '''
		raise NotImplementedError()

	def close(self):
		''' Stop the server, terminating self.run '''
		raise NotImplementedError()

	@property
	def closed(self):
		raise NotImplementedError()

	@property
	def properties(self):
		result = {}
		for name in dir(self):
			if name != "properties":
				result[name] = getattr(self, name)
		return result
