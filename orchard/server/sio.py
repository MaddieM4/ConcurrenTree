# Socket.IO BCP server

import gevent

from ConcurrenTree.util.server import socket_io as io
from ConcurrenTree.model.bcp.connection import BCPConnection, QueuePair
from ConcurrenTree.model.bcp.ext import authup, data

class SocketIOServer(io.Server):
	def __init__(self, port=9091, auth=None):
		io.Server.__init__(self)
		self.port = port
		self.auth = auth
		self.authorizer = authup.AuthUP(self.auth, onlogin)

	def on_connect(self, client):
		print client, 'connected'
		pair = QueuePair()[0]
		client.bcp = BCPConnection(pair, [self.authorizer])
		client.bcp._send = client.send
		client.greenlet = gevent.spawn(client.bcp.run)

	def on_message(self, client, message):
		client.bcp.inject(message)

	def run(self):
		self.listen(self.port)

def onlogin(conn, username, docs):
	# Load new extensions and make login unavailable
	conn.clear_extensions()
	conn.load_extension([
		data.Data(docs)
	])
