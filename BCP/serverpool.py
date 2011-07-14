from threading import Lock, Thread
from Queue import Queue

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

	def start(self, cls, *args, **kwargs):
		''' Add a server to the pool '''
		server = cls(*args, **kwargs)
		thread = Thread(target=server.run)
		thread.start()
		with self.lock:
			self.check_closed()
			self.servers.append((server, thread, []))

	def run(self):
		''' Run the pool, allowing interserver communication '''
		while not self.closed:
			with self.lock:
				s = 0
				while s < len(self.servers):
					if self.server(s).closed:
						del self.servers[s]
					else:
						self.process_server(s)
						s += 1

	def process_server(self, i):
		# Accept new connections
		for conn in self.server(i).starting():
			self.connect(i, conn)
		# Scan through connections
		c = 0
		while c < len(self.connections(i)):
			conn = self.connections(i)[c]
			conn.exchange()
			# Do something with the log, according to policy
			if conn.closed:
				del self.servers[i][2][c]
			else:
				c += 1

	def connect(self, server, queue):
		# use server.policy() here somewhere, for extensions/log
		conn = Connection(self.doc, self.auth, queue)
		self.servers[server][2].append(conn)

	def server(self, index):
		return self.servers[index][0]

	def thread(self, index):
		return self.servers[index][1]

	def connections(self, index):
		return self.servers[index][2]

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
	''' A Server policy is a bit like a config file. '''
	def __init__(self):
		self.input = {}
		self.output = {}
