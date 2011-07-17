''' 
	A class that lets you stack services according to
	configurations.
'''

from BCP.serverpool import ServerPool, Policy

class StackServer(ServerPool):
	def __init__(self, configstring=""):
		self.services = {}
		self.configure(configstring)
		self.policy = Policy()

	def configure(self, configstring):
		# tokenize
		tokens = configstring.split()
		while tokens:
			tokens = self.config_one(tokens)

	def config_one(self, tokens):
		if tokens[0] != "service":
			raise SyntaxError("StackServer service definitions must begin with keyword 'service'")
		try:
			servicename = tokens[1]
		except IndexError:
			raise SyntaxError("'service' keyword must be followed by a service name")
		tokens = tokens[2:]
		try:
			timeout = tokens.index("timeout")
		except ValueError:
			raise SyntaxError("Service definition must end in 'timeout' keyword")
		if timeout % 2 != 0:
			raise SyntaxError("Providers must be defined as a series of 'name escalatetimeout' pairs")
		prov = tokens[:timeout]
		providers = []
		try:
			for i in range(0,len(prov),2):
				providers[i/2] = (prov[i], int(prov[i+1]))
		except ValueError:
			raise SyntaxError("escalatetimeout must be an integer number of milliseconds.")
		self.services[servicename] = Service(servicelist(servicename), providers)
		return tokens[timeout+1:] # TODO: "responds" keyword

	def run(self):
		pass

	def policy(self):
		pass

	def starting(self):
		pass

	def close(self):
		pass

class Service:
	def __init__(self, inputs = [], servers = []):
		self.inputs = inputs
		self.servers = servers

def servicelist(name):
	if name in _servicelist:
		return _servicelist[name]
	else:
		return [name]

_servicelist = {
	'live':['op','ad','select']
}
