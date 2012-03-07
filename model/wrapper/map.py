from wrapper import Wrapper

class MapWrapper(Wrapper):
	def __getitem__(self, i):
		return self.context[i]

	def __setitem__(self, i, v):
		self.opsink(self.context.set(i, v))

	def __delitem__(self, i):
		self.opsink(self.context.set(i, None))

	def update(self, d):
		for k in d:
			self[k] = d[k]
