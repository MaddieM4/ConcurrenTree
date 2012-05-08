from Queue import Queue, Empty

class ValidationQueue(object):
	'''
	Class capable of taking an iterable (even a generator) and
	acting as an iterable queue. Iteration will end - not stop -
	if you get to the end of the current contents of the internal
	queue, so expect to for-loop through an instance multiple times.

	>>> my_queue = ValidationQueue(xrange(1,5))
	>>> for i in my_queue:
	...     print i
	...     if i < 5:
	...         my_queue.add(i*2)
	1
	2
	3
	4
	2
	4
	6
	8
	4
	8
	8
	'''

	def __init__(self, source=[]):
		# Accepts any iterable as optional argument for initial data.
		self.source = source
		self.queue = Queue()

	def __iter__(self):
		return self.gen()

	def gen(self):
		# Returns the generator used by __iter__().
		for x in self.source:
			yield x
		self.source = []
		while True:
			try:
				yield self.queue.get_nowait()
			except Empty:
				return

	def add(self, obj):
		# Add an object to the internal queue.
		self.queue.put(obj)
