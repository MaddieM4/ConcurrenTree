from wrapper import Wrapper

class NumberWrapper(Wrapper):
	def __init__(self, node, opsink, unique=None):
		Wrapper.__init__(self, node, opsink)
		if unique:
			self.unique = unique
		else:
			self.unique = node.unique

	def __iadd__(self, other):
		self.opsink(self.context.delta(other, self.unique))
		return self

	def __isub__(self, other):
		self += -other
		return self

	def __int__(self):
		return int(self.value)

	def __long__(self):
		return long(self.value)

	def __float__(self):
		return float(self.value)
