from threading import Lock

class Policy:
	''' 
		A Server policy is a bit like a config file. It
		defines what will be inputted to and outputted from
		a Connection. It does this with functions that
		are called on the appropriate message types by the
		ServerPool.

		callback(msgdict, connection, broadcast):
			# msgdict - the dict representation of a BCP message
			# connection - the BCP.Connection in question
			# broadcast - single-argument function to broadcast a msgdict to the environment
	'''
	def __init__(self, inputs = {}, outputs = {}):
		self.inputs = SubPolicy(inputs)
		self.outputs = SubPolicy(outputs)

	def input(self, message, connection, broadcast):
		''' Function to recieve a message from a Connection '''
		return self.run(self.inputs, message, connection, broadcast)

	def output(self, message, connection, broadcast):
		''' Function to output to a Connection '''
		return self.run(self.outputs, message, connection, broadcast)

	def run(self, ivo, message, *args):
		try:
			func = ivo[message['type']]
		except KeyError:
			print "No default in subpolicy"
			return None
		return func(message, *args)

class SubPolicy(dict):
	''' Contains functions keyed on message type, is thread-safe '''
	def __init__(self, values={}):
		super(SubPolicy, self).__init__(self)
		self.lock = Lock()
		self.update(values)
		self._default = None

	def __getitem__(self, i):
		with self.lock:
			if not i in self and self._default:
				return self._default
			else:
				return dict.__getitem__(self, i)

	def __setitem__(self, i, y):
		# validate value
		if type(i)!=str:
			raise TypeError("SubPolicy keys must be strings")
		if not hasattr(y,"__call__"):
			raise TypeError("SubPolicy values must be callable")
		with self.lock:
			dict.__setitem__(self, i, y)

	def __delitem__(self, i):
		with self.lock:
			dict.__delitem__(self, i)

	def set_multi(self, value, *args, **kwargs):
		if "keys" in kwargs:
			args += kwargs["keys"]
		for i in args:
			self[i] = value

	def bloom(self, source, *args, **kwargs):
		if "keys" in kwargs:
			args += kwargs["keys"]
		self.set_multi(self[source], keys=args)

	@property
	def default(self):
		''' Use _default within the class to avoid deadlocks! '''
		with self.lock:
			return self._default

	@default.setter
	def default(self, value):
		if not hasattr(value, "__call__"):
			raise TypeError("SubPolicy values must be callable")
		with self.lock:
			self._default = value

def BlankPolicy():
	''' Passes everything, as opposed to a policy with no defaults, which passes nothing '''
	new = Policy()
	new.inputs.default = lambda message, conn, broadcast: broadcast(message)
	new.outputs.default = lambda message, conn, broadcast: conn.queue.server_push(message)
