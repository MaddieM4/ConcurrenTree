''' 
	A conceptual primer on text concurrency.

	In any concurrent text system, you have two competing inputs -
	the network, and the user. While your goal is to make it appear
	like both are working asynchronously, some part of your program
	must stitch the two together, and it has to be a part that's not
	likely to be a bottleneck.

	We've found that the best way to do this is to intercept keystrokes,
	queue them up on one side (and network operations on the other),
	and manually apply both to the display as the man in the middle
	works through both queues. Since network ops already have variable
	latency, and the user expects their own keystrokes to register
	instantly, we always work fully through the user queue before
	displaying network ops, and check it for new data after applying
	each net op.

	This handler class is pretty basic and general, so you can use it
	however you want. It expects you to subclass ConcurrenTree.display.
	Display for objects that want to communicate with CTree docs.

	Docnames are arbitrary strings. Preventing name collisions is up
	to your implementation.
'''

import Queue
import threading
from time import sleep
from display import Display

class Handler:
	def __init__(self):
		self.stopflag = False
		self.documents = {}
		self.displays = {}
		self.netiq = Queue.Queue()
		self.netoq = Queue.Queue()
		self.userq = Queue.Queue()
		self.thread = None
		self.lock = threading.Lock()

	def replace(self, docname, start, end, value):
		self.userq.put((docname, start, end, value))

	def add_display(self, docname, display):
		with self.lock:
			if not docname in self.documents:
				raise ValueError("Document '%s' is not loaded in the handler" % docname)
			elif isinstance(display, Display):
				self.displays[docname].add(display)
			else:
				raise TypeError(str(type(display))+" is not a descendant of ConcurrenTree.display.Display")

	def remove_display(self, docname, display):
		with self.lock:
			if docname in self.displays:
				self.displays[docname].remove(display)
			else:
				raise ValueError("Document '%s' is not loaded in the handler" % docname)

	def __getitem__(self, docname):
		with self.lock:
			return self.documents[docname]

	def __setitem__(self, docname, document):
		with self.lock:
			self.documents[docname] = document
			self.displays[docname] = set()

	def __delitem__(self, docname):
		with self.lock:
			del self.documents[docname]
			del self.displays[docname]

	def process(self):
		while not self.stopflag:
			with self.lock:
				while not self.netiq.empty():
					# clear out all user stuff first
					while not self.userq.empty():
						# process user action
					# process network operation
			sleep(.05)

	def start(self):
		if not self.thread:
			self.thread = threading.Thread(target = self.process)
			self.thread.setDaemon(True)

	def stop(self):
		if self.thread:
			self.stopflag=True
			self.thread.join()
			self.thread = None

	def get_network_out(self):
		return self.netoq.get()
