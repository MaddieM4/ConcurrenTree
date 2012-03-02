import node
import json

class NumberNode(node.Node):

	def __init__(self, value, unique):
		node.Node.__init__(self)
		self._value = str(value) # Store value as string to avoid loss of precision
		self.unique = int(unique)
		self._children = [node.ChildSet(NumberNode)]

	# Node interface

	@property
	def value(self):
		return self._value

	@property
	def key(self):
		return self.keysum("n%d/%d" % (
			int(json.loads(self.value)),
			self.unique
		))

	def flatten(self):
		result = json.loads(self.value)
		for i in self._children[0].values:
			result += i.flatten()
		return result

	def _get(self, pos, key):
		if pos != 0:
			raise IndexError("NumberNode only has children at position 0.")
		return self._children[0][key]

	def _put(self, pos, obj):
		if pos != 0:
			raise IndexError("NumberNode only has children at position 0.")
		self._children[0].insert(obj)

	def _delete(self, pos):
		raise node.Undelable("NumberNode does not support deletion")

	@property
	def deletions(self):
		return []

	def resolve(self, addr):
		if len(addr)==0:
			return self
		else:
			return self.get(0, addr[0]).resolve(addr[1:])

	# Extra

	def head(self):
		# return (addr, node) for deepest node
		winner = ([], self)
		for i in self._children[0]:
			addr, n = self.get(0,i).head()
			addr = [i] + addr
			if len(addr) > len(winner[0]):
				winner = addr, n
		return winner
