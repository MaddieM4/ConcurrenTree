'''
	UDPJack

	IPv6 UDP jack, currently programmed quick and dirty to serve forever.
'''

import jack
import socket
import message

class UDPJack(jack.Jack):
	def __init__(self, router, host='::', port=3972):
		jack.Jack.__init__(self, router, ('udp', (host, port)))
		self.address = (host, port, 0, 0)
		self.sock = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
		self.sock.bind(self.address)

	def route(self, msg):
		# Send message to somewhere
		location = msg.addr[1]
		addr = (location[0], location[1], 0,0)
		self.sock.sendto(str(message), addr)

	def run(self):
		while True:
			data = self.sock.recv(message.PACKET_SIZE)
			self.send(data)
