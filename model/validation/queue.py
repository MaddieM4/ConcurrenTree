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

	def __init__(self, source=[], filters=[]):
		# Accepts any iterable as optional argument for initial data.
		self.source = source.__iter__()
		self.queue = Queue()
		self.filters = list([])

	def __iter__(self):
		return self.gen()

	def gen(self):
		# Returns the generator used by __iter__().
		while True:
			yield self.pop()

	def pop(self):
		try:
			return self.source.next()
		except StopIteration:
			pass
		try:
			return self.queue.get_nowait()
		except Empty:
			raise StopIteration

	def add(self, obj):
		# Add an object to the internal queue.
		self.queue.put(obj)

	def filter(self, obj):
		for i in self.filters:
			obj = i(obj)
			if obj==None:
				break
		if obj!=None:
			self.add(obj)
