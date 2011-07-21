class Pool:
	''' A BCP "router" that forwards messages between connections. '''
	def __init__(self, docHandler, authHandler):
		self.lock = Lock()
		self.stoprunning = False
		self.connections = []
		self.docs = docHandler
		self.auth = authHandler

	def connect(self, socket):
		''' Add a connection to the Pool '''
		with self.lock:
			conn = Connection(self.docs, self.auth, socket, log=['op','ad'])
			self.connections.append(conn)
			return conn

	def remove(self, conn):
		''' Remove a connection. May be a socket or a BCP.Connection '''
		with self.lock:
			kill = conn
			for i in self.connections:
				if i.socket==conn:
					kill = i
			self.connections.remove(kill)

	def run(self):
		while True:
			sleep(.001)
			with self.lock:
				for conn in self.connections:
					if self.stoprunning:
						return
					conn.exchange()
					# process connection log
					self.spread(conn)

	def spread(self, conn):
		ads = []
		while not conn.log.empty():
			obj = conn.log.get()
			
		for other in self.others(conn):
			

	def others(self, conn):
		result = self.connections
		result.remove(conn)
		return result

