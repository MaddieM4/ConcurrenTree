class BaseStorage(object):

	def __init__(self, find=None):
		''' 
			Find is an optional callback. It takes a docname, attempts to
			retrieve the document from remote sources, and either succeeds
			and returns a Document object or fails and raises NameError.

			This should block until a blank Document is ready and the host
			has confirmed that you have access to the doc. This document 
			will be stored for you in the correct docname slot.
		'''
		self.events = []
		self._find = find

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

	# Events

	def subscribe(self, docname):
		self.events.append(("sub", docname, True))
		self[docname].subscribed = True

	def unsubscribe(self, docname):
		self.events.append(("sub", docname, False))
		self[docname].subscribed = False

	def op(self, docname, op):
		self.events.append(("op", docname, op))
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
