import ConcurrenTree.util.hasher as hasher
import ConcurrenTree.util.server.websocket as websocket

from server import *

class WSConnection(websocket.WebSocket):
	def __init__(self, client, server):
		super(WSConnection, self).__init__(client, server)
		self.dq = dq.DQ()

	def onmessage(self, data):
		self.dq.client_push(data)

	def onsweep(self):
		while True:
			try:
				self.send(self.dq.client_pull(timeout=0))
			except dq.Empty:
				break

	def close(self):
		super(WSConnection, self).close()
		self.dq.client_push(0)

class WebSocketServer(Server):
	def __init__(self, port=9091):
		self.closed = False
		self.port = port
		self.server = websocket.WebSocketServer('localhost',port, WSConnection)
		self._policy = Policy()

	def run(self):
		startmessage("WebSocket", self.port)
		#print "WebSocket server starting on port %d" % self.port
		self.server.listen(5)
		print "WebSocket server terminating"

	def starting(self):
		news = []
		while True:
			try:
				news.append(self.server.queue.get_nowait().dq)
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
