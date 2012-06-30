from wrapper import Wrapper

class ListWrapper(Wrapper):
	def __getitem__(self, i):
		if type(i) == slice:
			return [self[x] for x in range(*i.indices(len(self)))]
		from ConcurrenTree.wrapper import make
		addr, n = self.context.get(i)
		return make(n, self.childsink(addr))

	def __setitem__(self, i, x):
		del self[i]
		self.insert(i, x)

	def __delitem__(self, i):
		self.opsink(self.context.delete(i,1))

	def __delslice__(self, i, k):
		l = len(self)
		i %= l
		k %= l
		size = max(k-i,0)
		self.opsink(self.context.delete(i, size))

	def __len__(self):
		return len(self.value)

	def __str__(self):
		return self.value

	def __add__(self, y):
		return self.value+y

	def __iadd__(self, y):
		# self += other
		self.insert(len(self), y)
		return self

	def insert(self, pos, value):
		self.opsink(self.context.insert(pos, value))

	def append(self, value):
		self.insert(len(self), value)
