'''
	UDPJack

	IPv6 UDP jack, currently programmed quick and dirty to serve forever.
'''

import jack
import socket
import message

class UDPJack(jack.Jack):
	def __init__(self, router, host='::', port=3972, ipv=6):
		if ipv==6:
			ifacetype = "udp"
			self.address = (host, port, 0, 0)
			sockfamily = socket.AF_INET6
		else: 
			ifacetype = "udp4"
			self.address = (host, port)
			sockfamily = socket.AF_INET

		jack.Jack.__init__(self, router, (ifacetype, (host, port)))
		self.sock = socket.socket(sockfamily, socket.SOCK_DGRAM)
		self.sock.bind(self.address)
		self.closed = False

	def route(self, msg):
		# Send message to somewhere
		location = msg.addr[1]
		if self.ifacetype == 'udp':
			addr = (location[0], location[1], 0,0)
		else:
			addr = (location[0], location[1])
		print "UDPJack out:", len(str(msg)), "/", self.sock.sendto(str(msg), addr)

	def run(self):
		while not self.closed:
			data = self.sock.recv(message.PACKET_SIZE)
			self.recv(data)

	def run_threaded(self):
		import thread
		self.thread = thread.start_new_thread(self.run, ())

	def close(self):
		self.closed = True
