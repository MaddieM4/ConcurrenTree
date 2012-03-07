from wrapper import Wrapper

class StringWrapper(Wrapper):
	def __getitem__(self, i):
		return self.value[i]

	def __setitem__(self, i, x):
		pass

	def __delitem__(self, i):
		self.opsink(self.context.delete(i,1))
