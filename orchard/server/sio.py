# Socket.IO BCP server

import gevent

from ConcurrenTree.util.server import socket_io as io
from ConcurrenTree.model.bcp.connection import BCPConnection, QueuePair

class SocketIOServer(io.Server):
	def __init__(self, port=9091, docs=None, auth=None):
		io.Server.__init__(self)
		self.port = port
		self.docs = docs
		self.auth = auth

	def on_connect(self, client):
		print client, 'connected'
		pair = QueuePair()[0]
		client.bcp = BCPConnection(self.docs, self.auth, pair)
		client.bcp._send = client.send
		client.greenlet = gevent.spawn(client.bcp.run)

	def on_message(self, client, message):
		client.bcp.inject(message)

	def run(self):
		self.listen(self.port)
