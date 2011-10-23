import node

class TrinaryNode(node.Node):
	def __init__(self, value):
		if value in (True, False, None):
			self._value = value
		else:
			raise ValueError("A TrinaryNode can only represent True, False, or None")

	@property
	def value(self):
		return self._value

	@property
	def key(self):
		if self.value == True:
			return "/true"
		elif self.value == False:
			return "/false"
		else:
			return "/null"

	def flatten(self):
		return self.value

	def get(self, pos, key):
		raise IndexError("TrinaryNodes can contain no children")

	def put(self, pos, obj):
		raise IndexError("TrinaryNodes can contain no children")

	def instruct(self):
		pass

	def proto(self):
		return self.value
