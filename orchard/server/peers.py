from server import *
from threading import Lock
from ConcurrenTree.model.bcp.connection import BCPConnection

import socket
import select

class PeerSocket:
	def __init__(self, socket, docs, cycleflag):
		self.closed = False
		self.socket = socket
		self.cycleflag = cycleflag
		
		self.connection = BCPConnection(docs, None)
		self.dq = self.connection.ioqueue

	def recv(self):
		data = self.socket.recv(1024)
		if data:
			print "Peer receiving:",repr(data)
			self.dq.server_push(data)
			self.cycleflag()
		else:
			self.close()

	def process(self):
		while True:
			try:
				data = self.dq.server_pull(timeout=0)
				print "Peer sending:",repr(data)
				self.socket.sendall(data)
				self.cycleflag()
			except dq.Empty:
				break

	def close(self):
		print "Peersocket closing itself"
		#self.process()
		self.dq.server_push(0)
		self.socket.close()
		self.closed = True

class Peers(Server):
	def __init__(self, port=9090, docs = None):
		self.lock = Lock()
		with self.lock:
			self.socket = socket.socket() # defaults to needed properties
		        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.socket.bind(('',port))
			self.closed = False
			self.unread = []
			self.peers = {}
			self._policy = PeerPolicy()
			self.docs = docs

	def run(self):
		startmessage('Peer', self.socket.getsockname()[1])
		self.socket.listen(4)
		while not self.closed:
			for i in self.peers:
				self.peers[i].process()
			self.clean()
			Rlist, Wlist, Xlist = select.select(self.listeners, [], self.listeners, 0.1)
			for ready in Rlist:
				if ready == self.socket:
					client, address = self.socket.accept()
					self.connect_socket(client)
				else:
					print "PeerSocket ready for reading (%d)" % ready
					self.peers[ready].recv()
			for failed in Xlist:
				if failed==self.socket:
					print "Peer host socket broke"
					self.close()
		print "Peer Server shutting down"

	def connect(self, address):
		if type(address)==str:
			address = address.split(':')
			address[1] = int(address[1])
		address = tuple(address)
		print "Connecting to peer:", address
		newsock = socket.socket()
		newsock.connect(address)
		self.connect_socket(newsock)

	def connect_socket(self, client):
		newpeer = self.peers[client.fileno()] = PeerSocket(client, self.docs, self.cycleflag)
		print "New peer connection:", client.getpeername()
		with self.lock:
			self.unread.append(newpeer.connection)

	def starting(self):
		with self.lock:
			unread, self.unread = self.unread, []
			return unread

	def policy(self):
		return self._policy

	def close(self):
		for peer in self.peers:
			self.peers[peer].close()
		self.closed = True

	@property
	def address(self):
		try:
			return self.socket.getsockname()
		except:
			return ('',0)

	@property
	def port(self):
		return self.address[1]

	@property
	def properties(self):
		return {
			"name":"PeerServer",
			"closed":self.closed,
			"connect":self.connect,
			"port":self.port,
			"address":self.address
		}

	def clean(self):
		i = 0
		keys = self.peers.keys()
		while i<len(keys):
			if self.peers[keys[i]].closed:
				del self.peers[keys[i]]
			i+=1

	@property
	def listeners(self):
		return [self.socket]+[x for x in self.peers]

class PeerPolicy(Policy):
	def __init__(self):
		Policy.__init__(self)
		self.inputs.default = lambda msg, conn, bcast: bcast(msg)
		self.outputs.default = lambda msg, conn, bcast: conn.queue.server_push(msg)
