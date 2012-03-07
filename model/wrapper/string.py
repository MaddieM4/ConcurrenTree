from wrapper import Wrapper

class StringWrapper(Wrapper):
	def __getitem__(self, i):
		return self.value[i]

	def __setitem__(self, i, x):
		raise NotImplementedError("__setitem__ not written yet for StringWrapper")

	def __delitem__(self, i):
		self.opsink(self.context.delete(i,1))

	def __getslice__(self, i, k):
		return self.value[i:k]

	def __delslice__(self, i, k):
		l = len(self)
		i %= l
		k %= l
		size = max(k-i,0)
		self.opsink(self.context.delete(i, size))

	def __len__(self):
		return len(self.value)

	def __add__(self, y):
		return self.value+y

	def __iadd__(self, y):
		# self += other
		self.insert(len(self), y)

	def insert(self, pos, value):
		self.opsink(self.context.insert(pos, value))
