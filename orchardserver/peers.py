import orchardserver
from BCP.serverpool import PoolServer
import BCP.doublequeue as dq
from threading import Lock

import socket
import select

class PeerSocket:
	def __init__(self, socket):
		self.closed = False
		self.socket = socket
		self.dq = dq.DQ()

	def recv(self):
		data = self.socket.recv(1024)
		if data:
			self.dq.client_push(data)
		else:
			self.close()

	def process(self):
		while True:
			try:
				self.socket.sendall(self.dq.client_pull(timeout=0))
			except dq.Empty:
				break

	def close(self):
		print "Peersocket closing itself"
		#self.process()
		self.dq.client_push(0)
		self.socket.close()
		self.closed = True

class Peers(PoolServer):
	def __init__(self, port=9090):
		self.lock = Lock()
		self.socket = socket.socket() # defaults to needed properties
	        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.socket.bind(('',port))
		self.closed = False
		self.peers = {}
		self.unread = []

	def run(self):
		orchardserver.startmessage('Peer', self.socket.getsockname()[1])
		self.socket.listen(4)
		while not self.closed:
			for i in self.peers:
				self.peers[i].process()
			self.clean()
			Rlist, Wlist, Xlist = select.select(self.listeners, [], self.listeners, 0.1)
			for ready in Rlist:
				if ready == self.socket:
					client, address = self.socket.accept()
					newpeer = self.peers[client.fileno()] = PeerSocket(client)
					print "New peer connection (%d)" % client.fileno()
					with self.lock:
						self.unread.append(newpeer.dq)
				else:
					print "PeerSocket ready for reading (%d)" % ready
					self.peers[ready].recv()
			for failed in Xlist:
				if failed==self.socket:
					print "Peer host socket broke"
					self.close()
		print "Peer Server shutting down"

	def starting(self):
		with self.lock:
			unread = self.unread
			self.unread = []
			return unread

	def close(self):
		for peer in self.peers:
			self.peers[peer].close()
		self.closed = True

	def clean(self):
		i = 0
		keys = self.peers.keys()
		while i<len(keys):
			if self.peers[keys[i]].closed:
				del self.peers[keys[i]]
			else:
				i+=1

	@property
	def listeners(self):
		return [self.socket]+[x for x in self.peers]
