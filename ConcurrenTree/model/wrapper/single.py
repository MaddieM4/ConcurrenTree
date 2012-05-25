from wrapper import Wrapper

class SingleWrapper(Wrapper):
	def get(self):
		from ConcurrenTree.model.wrapper import make
		addr, n = self.context.get()
		if addr == None:
			return None
		return make(n, self.childsink(addr))

	def set(self, value):
		self.opsink(self.context.set(value))

	def __repr__(self):
		return "ws<%r>" % self.value
