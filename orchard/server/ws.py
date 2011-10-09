import ConcurrenTree.util.hasher as hasher
import ConcurrenTree.util.server.websocket as websocket
from ConcurrenTree.model.bcp.connection import BCPConnection

from server import *

class WSConnection(websocket.WebSocket):
	def __init__(self, client, server):
		super(WSConnection, self).__init__(client, server)
		self.connection = BCPConnection(server.docs, None)
		self.dq = self.connection.ioqueue

	def onmessage(self, data):
		print "Websocket receiving data:", data
		self.dq.server_push(data)

	def onsweep(self):
		while True:
			try:
				self.send(self.dq.server_pull(timeout=0))
			except dq.Empty:
				break
		self.connection.cycle()

	def close(self):
		super(WSConnection, self).close()
		self.dq.server_push(0)

class WebSocketServer(Server):
	def __init__(self, port=9091, docs = None):
		self.docs = docs
		self.closed = False
		self.port = port
		self.server = websocket.WebSocketServer('localhost',port, WSConnection)
		self.server.docs = docs
		self._policy = WSPolicy()

	def run(self):
		startmessage("WebSocket", self.port)
		#print "WebSocket server starting on port %d" % self.port
		self.server.listen(5)
		print "WebSocket server terminating"

	def starting(self):
		news = []
		while True:
			try:
				news.append(self.server.queue.get_nowait().connection)
			except dq.Empty:
				break
		return news

	def policy(self):
		return self._policy

	def close(self):
		self.server.running = False

	@property
	def properties(self):
		return {
			"name":"WebSocket",
			"port":self.port,
			"closed":self.closed
		}

class WSPolicy(Policy):
	def __init__(self):
		Policy.__init__(self)
		self.inputs.default = lambda msg, conn, bcast: bcast(msg)
		self.outputs.default = lambda msg, conn, bcast: conn.queue.server_push(msg)
