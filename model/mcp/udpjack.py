'''
	UDPJack

	IPv6 UDP jack, currently programmed quick and dirty to serve forever.
'''

import jack
import socket

class UDPJack(jack.Jack):
	def __init__(self, router, address=('::', 3972, 0, 0)):
		jack.Jack.__init__(self, router)
		self.address = address
		self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
		self.sock.bind(self.address)

	def route(self, msg):
		# Send message to somewhere
		location = msg.addr[1]
		addr = (location[0], location[1], 0,0)
		self.sock.sendto(str(message), addr)

	def run(self):
		while True:
			data, addr = self.sock.recvfrom(4096)
			self.send(data)
