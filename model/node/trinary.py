import node

class TrinaryNode(node.Node):
	def __init__(self, value):
		if value in (True, False, None):
			self._value = value
		else:
			raise ValueError("A TrinaryNode can only represent True, False, or None")

	# Node interface

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
		raise node.Ungetable("TrinaryNodes can contain no children")

	def put(self, pos, obj):
		raise node.Unputable("TrinaryNodes can contain no children")

	def delete(self):
		raise node.Undelable("TrinaryNodes can contain no children")

	@property
	def deletions(self):
		return []

	@property
	def children(self):
		return {}
