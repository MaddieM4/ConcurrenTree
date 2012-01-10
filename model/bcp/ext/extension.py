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

	def require(self, conn, arg, obj):
		if not arg in obj:
			self.error(conn, 452, 'Missing required argument: "%s"' % arg, arg)

	def error(self, conn, *args, **kwargs):
		''' Send an error message and raise a SilentFail '''
		conn.error(*args, **kwargs)
		raise SilentFail()

class TryAnother(KeyError):
	pass

class SilentFail(StopIteration):
	pass
