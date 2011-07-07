''' 
	The live node functionality in Orchard is a class
	separate from the main script, even though during early
	development it will be more or less the only functionality.

	This is to simplify and compartmentalize the pieces of Orchard,
	With command-line/controller/main separate from the live
	servers, separate from the piece that manages cold storage.

	Orchard Live handles the HTTP server, Websocket server, and
	the BCP server (which speaks directly to live peers and to
	websocket clients alike).
'''

import socket
import webbrowser
from threading import Thread

# TODO - HTTP server in a separate thread

import BCP
import storage

class Live:
	def __init__(self, port, wsport, initpeers=[]):
		# Create servers and link them up
		self.initpeers = initpeers

	def run(self):
		# Start serving
		# Connect to initial peers
		pass
