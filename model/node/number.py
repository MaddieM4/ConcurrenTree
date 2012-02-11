import node
import json

class NumberNode(node.Node):

	def __init__(self, value, unique):
		self._value = str(value) # Store value as string to avoid loss of precision
		self.unique = int(unique)
		self._children = node.ChildSet(NumberNode)

	# Node interface

	@property
	def value(self):
		return self._value[0]

	@property
	def key(self):
		return self.keysum("n"+str(
			int(json.loads(self.value)) + self.unique
		))

	def flatten(self):
		result = json.loads(self.value)
		for i in self._children.values:
			result += i.flatten()
		return result

	def get(self, pos, key):
		if pos != 0:
			raise IndexError("NumberNode only has children at position 0.")
		return self._children[key]

	def put(self, pos, obj):
		if pos != 0:
			raise IndexError("NumberNode only has children at position 0.")
		self._children.insert(obj)

	def delete(self, pos):
		raise node.Undelable("NumberNode does not support deletion")

	@property
	def deletions(self):
		return []

	def proto(self):
		pass # TODO
