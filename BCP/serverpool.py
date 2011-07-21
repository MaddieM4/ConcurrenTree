from threading import Lock, Thread
from Queue import Queue, Empty
import traceback

from connection import Connection

class ServerPool:
	''' A collection of server objects that provide real
	or virtual peers. '''

	def __init__(self, docHandler, authHandler):
		self.doc = docHandler
		self.auth = authHandler

		self.servers = []
		self.lock = Lock()
		self.closed = False
		self.env = [[],[]]

	def start(self, cls, *args, **kwargs):
		''' Add a server to the pool '''
		server = cls(*args, **kwargs)
		thread = Thread(target=server.run)
		thread.start()
		with self.lock:
			self.check_closed()
			self.servers.append((server, thread, []))
			return server

	def run(self):
		''' Run the pool, allowing interserver communication '''
		while not self.closed:
			with self.lock:
				s = 0
				while s < len(self.servers):
					if self.server(s).closed:
						del self.servers[s]
					else:
						try:
							self.process_server(s)
						except Exception as e:
							self.crash(e)
						s += 1

	def process_server(self, i):
		policy = self.server(i).policy()
		# Accept new connections
		for conn in self.server(i).starting():
			self.connect(i, conn, policy.extensions)
		def broadcast(msg):
			self.buffer.append(msg)
		# Scan through connections
		c = 0
		while c < len(self.connections(i)):
			try:
				conn = self.connections(i)[c]
				conn.exchange()
				# Do something with the log, according to policy
				while True:
					try:
						msg = conn.log.get_nowait()
						print "receiving message:  ", i, c, msg
						policy.output(msg, conn, broadcast)
					except Empty:
						break
				for msg in self.lastbuffer:
					policy.input(msg, conn, broadcast)
				if conn.closed:
					del self.servers[i][2][c]
				else:
					c += 1
			except Exception as e:
				self.crash(e)

	def connect(self, server, queue, extensions = {}):
		conn = Connection(self.doc, self.auth, queue, extensions=extensions, log="*")
		self.servers[server][2].append(conn)

	def server(self, index):
		return self.servers[index][0]

	def thread(self, index):
		return self.servers[index][1]

	def connections(self, index):
		return self.servers[index][2]

	@property
	def buffer(self):
		''' The part of the environment currently being edited '''
		return self.env[0]

	@property
	def lastbuffer(self):
		''' The read-only results of the last env cycle '''
		return self.env[1]

	def buffer_flip(self):
		self.env = [self.env[1], []]

	def crash(self, e):
		''' 
			Process an error in a way that will not
			bork the thread. 

			Warning: it will stop any error except
			KeyboardInterrupt and never raise it,
			therefore any code after the except
			statement that calls self.crash(e)
			will run whether an error occurs or not.
			This is normal behavior for except
			statements, I'm just remindin' ya.
		'''
		traceback.print_exc()
		if type(e)==KeyboardInterrupt:
			self.close()

	def close(self):
		with self.lock:
			self.check_closed()
			self.closed = True
			for i in self.servers:
				i[0].close()
			for i in self.servers:
				i[1].join()

	def check_closed(self):
		if self.closed:
			raise ClosedError("ServerPool is closed")

class PoolServer:
	''' Base class for ServerPool Servers. '''
	def run(self):
		''' Start the server running '''
		raise NotImplementedError()

	def starting(self):
		''' 
		Return a list of BCP.doublequeue.DQ() objects, 
		one for each NEW connection. Do not include
		connections that have already been returned
		through this function. 

		The Queues you return should contain strings
		until the connection is terminated, at which
		point your server should put the integer 0, or
		the integer BCP error code associated with the
		termination.

		'''
		raise NotImplementedError()

	def policy(self):
		''' Return a BCP.Policy() object '''
		raise NotImplementedError()

	def close(self):
		''' Stop the server, terminating self.run '''
		raise NotImplementedError()

	@property
	def closed(self):
		raise NotImplementedError()

class Policy:
	''' 
		A Server policy is a bit like a config file. It
		defines what will be inputted to and outputted from
		a BCP.Connection. It does this with functions that
		are called on the appropriate message types by the
		ServerPool.

		callback(msgdict, connection, broadcast):
			# msgdict - the dict representation of a BCP message
			# connection - the BCP.Connection in question
			# broadcast - single-argument function to broadcast a msgdict to the environment
	'''
	def __init__(self, inputs = {}, outputs = {}, extensions = {}):
		self.inputs = SubPolicy(inputs)
		self.outputs = SubPolicy(outputs)
		self.extensions = SubPolicy(extensions)

	def input(self, message, *args):
		''' Function to broadcast a message to a Connection '''
		return self.run(self.inputs, message, *args)

	def output(self, message, *args):
		''' Function to run on Connection logs '''
		return self.run(self.outputs, message, *args)

	def run(self, ivo, message, *args):
		try:
			func = ivo[message['type']]
		except KeyError:
			return None
		return func(message, *args)

class SubPolicy(dict):
	''' Contains functions keyed on message type, is thread-safe '''
	def __init__(self, values={}):
		super(SubPolicy, self).__init__(self)
		self.lock = Lock()
		self.update(values)

	def __getitem__(self, i):
		with self.lock:
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
			args += kwargs['keys']
		for i in args:
			self[i] = value

	def bloom(self, source, *args, **kwargs):
		if "keys" in kwargs:
			args += kwargs['keys']
		for i in args:
			self[i] = self[source]
