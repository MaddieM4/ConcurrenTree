from doublequeue import DQ, Empty

class Connection:
	def __init__(self):
		self.queue = DQ()
		self.ioqueue = DQ()
		self.buffer = ""
		self.uniquesource = None
		self.closed = False

	def cycle(self):
		''' Read queues and process data '''
		flag = True
		while flag:
			if self.closed: return
			flag = self.read() or self.write()

	def read(self):
		''' Read from ioqueue and process buffer '''
		if self.closed:
			return False
		try:
			new = self.ioqueue.client_pull(0)
			if type(new) == int:
				self.close(new)
			else:
				self.cycleflag()
				buffer = self.incoming(self.buffer+new)
			return True
		except Empty:
			return False

	def write(self):
		''' Read from queue and output to IO '''
		if self.closed:
			return False
		try:
			out = self.queue.client_pull(0)
			if type(out) == int:
				self.close(out)
			else:
				self.cycleflag()
				result = self.outgoing(out)
				if type(result) in (str, unicode):
					self.ioqueue.client_push(result)
			return True
		except Empty:
			return False

	def incoming(self, value):
		''' Analyze buffer and return any unparseable tail '''
		raise NotImplementedError("Subclasses of Connection must define incoming()")

	def outgoing(self, msg):
		''' Analyze pool message, return string for IO '''
		raise NotImplementedError("Subclasses of Connection must define outgoing()")

	def getunique(self, key):
		if self.uniquesource:
			return self.uniquesource.getunique(key)
		else:
			raise NameError("No uniquesource defined for connection")

	def cycleflag(self):
		# override with function to request more cycles
		return True

	def close(self, code):
		self.closed = True
