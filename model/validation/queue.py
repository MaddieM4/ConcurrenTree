from Queue import Queue, Empty

class ValidatorQueue(object):
	'''
	Class capable of taking an iterable (even a generator) and
	acting as an iterable queue. Iteration will end - not stop -
	if you get to the end of the current contents of the internal
	queue, so expect to for-loop through an instance multiple times.

	>>> #from ConcurrenTree.model.validator import queue
	>>> my_queue = ValidatorQueue(xrange(1,5))
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
		self.source = source
		self.queue = Queue()
		self.generator = self.gen()

	def __iter__(self):
		return self

	def gen(self):
		for x in self.source:
			yield x
		self.source = []
		while True:
			try:
				yield self.queue.get_nowait()
			except Empty:
				return

	def next(self):
		return self.generator.next()

	def add(self, obj):
		self.queue.put(obj)
