class Extension(object):
	def __init__(self, name, callbacks, bound=False):
		self.name = name
		self.callbacks = callbacks
		self.bound = bound

	def process(self, conn, msg):
		obt = msg['type']
		if not obt in self.callbacks:
			raise TryAnother(obt)
		else:
			try:
				if self.bound:
					return self.callbacks[obt](conn, msg)
				else:
					return self.callbacks[obt](self, conn, msg)
			except SilentFail:
				return # Extension has handled it

class TryAnother(KeyError):
	pass

class SilentFail(StopIteration):
	pass
