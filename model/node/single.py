import node

class SingleNode(node.Node):
	def __init__(self):
		self.children = node.ChildSet()

	# Node interface

	@property
	def value(self):
		return ""

	@property
	def key(self):
		return "/single"

	def flatten(self):
		return self.children.head.flatten()

	def get(self, pos, key):
		if pos != 0:
			raise IndexError("SingleNode only has children at pos 0")
		return self.children[key]

	def put(self, pos, obj):
		if pos != 0:
			raise IndexError("SingleNode only has children at pos 0")
		self.children.insert(ob)

	def delete(self):
		raise node.Undelable("SingleNodes do not support deletion. Recursive set to null instead.")

	def proto(self):
		pass # TODO - protocol rep of adv types
