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
'''

import Queue

class Handler:
	def __init__(self):
		self.documents = {}
		self.displays = {}
		self.netiq = Queue.Queue()
		self.netoq = Queue.Queue()
		self.userq = Queue.Queue()

	def replace(self, docname, start, end, value):
		pass

