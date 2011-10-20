class Server:
	''' Base class for ServerPool Servers. '''
	def run(self):
		''' Start the server running '''
		raise NotImplementedError()

	def starting(self):
		''' 
		Return a list of Connection objects, 
		one for each NEW connection. Do not include
		connections that have already been returned
		through this function. Subclasses are cool.
		'''
		raise NotImplementedError()

	def policy(self):
		''' Return a Policy() object '''
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

	def cycleflag(self):
		''' Externally overrided function to request a Pool cycle '''
		return None
