import threading
import thread

class BaseStorage(object):

	def __init__(self, find=None, encryptor = None):
		''' 
			Find is an optional callback. It takes a docname, attempts to
			retrieve the document from remote sources, and either succeeds
			and returns a Document object or fails and raises NameError.

			This should block until a blank Document is ready and the host
			has confirmed that you have access to the doc. This document 
			will be stored for you in the correct docname slot.

			Encryptor should be an object with methods "encrypt" and 
			"decrypt", or None.
		'''
		self.events = []
		self._find = find
		self.encryptor = encryptor

		self.flushing = True
		self.needflush = threading.Event()
		self.flusherthread = thread.start_new_thread(self.flush_loop)

	def find(self, docname):
		if docname in self:
			return self[docname]

		if self._find:
			doc = self._find(docname)
			self[docname] = doc
			return doc
		else:
			raise NameError(docname)

	def flush(self):
		''' 
			Flush any caches to permanent storage.
		'''
		raise NotImplementedError()

	def flush_loop(self):
		while self.flushing:
			self.needflush.wait(5)
			if self.needflush.is_set():
				self.flush()
				self.needflush.clear()

	# Encryption

	def encrypt(self, str):
		if self.encryptor:
			return self.encryptor.encrypt(str)
		else:
			return str

	def decrypt(self, str):
		if self.encryptor:
			return self.encryptor.decrypt(str)
		else:
			return str

	# Events

	def event(self, typestr, docname, data):
		for ear in self.event_listeners:
			ear(typestr, docname, data)

	def op(self, docname, op):
		self.event("op", docname, op)
		self[docname].apply(op)

	# Dict access
	def __getitem__(self, i):
		if i in self:
			return self.get(i)
		else:
			raise KeyError(i)

	def __setitem__(self, i, v):
		return self.set(i, v)

	def __delitem__(self, i):
		return self.delete(i)

	def __contains__(self, i):
		return self.has(i)

	# Override

	def get(self, i):
		raise NotImplementedError()

	def set(self, i, v):
		raise NotImplementedError()

	def delete(self, i):
		raise NotImplementedError()

	def has(self, i):
		raise NotImplementedError()
