from ConcurrenTree.model import ModelBase, node
from address import Address

def validpos(tree, pos):
	if not (pos <= len(tree) and pos >= 0):
		raise IndexError(pos, len(tree), "0 <= %d <= %d not true!" % (pos, len(tree)))

class Instruction(ModelBase):
	''' General class for all instructions '''

	def __init__(self, value):
		''' Value is a list or Instruction. '''
		if isinstance(value, Instruction):
			self.fromother(value)
		else:
			# Process protocol instruction
			self.fromproto(value)

	def fromproto(self, value):
		''' Sets properties from list. '''
		# TODO: type checking
		value = list(value)
		self.code = value[0]
		self.address = Address(value[1])
		self.additional = value[2:]

	def fromother(self, other):
		''' Sets properties from other instruction. '''
		self.fromproto(other.proto())

	def apply(self, tree, checkfirst = False):
		''' Apply this instruction to a tree. Operation is responsible for calling sanitycheck before applying. '''
		# Resolve tree in question
		tree = self.address.resolve(tree)

		# Sanity check
		if checkfirst:
			self.sanitycheck(tree)

		# Branch based on insertion or deletion
		if self.isinsert:
			self._apply_insert(tree)
		else:
			self._apply_delete(tree)

	def _apply_delete(self, tree):
		for d in self.deletions:
			for i in range(d[0], d[1]+1):
				tree.delete(i)

	def _apply_insert(self, tree):
		vn = self.value_node
		try:
			tree.get(self.position, vn.key)
		except:
			tree.put(self.position, vn)

	def sanitycheck(self, tree):
		''' Check a tree to make sure this instruction can be applied. '''
		if self.isinsert:
			validpos(tree, self.position)
		else:
			for i in self.deletions:
				validpos(tree, i[0])
				validpos(tree, i[1])
				if i[0] > i[1]:
					raise ValueError("Backwards deletion range [%d, %d]" % i)

	def proto(self):
		''' Protocol representation '''
		return [self.code, self.address.proto()] + self.additional

	@property
	def isinsert(self):
		return self.code != 0

	@property
	def position(self):
		return self.additional[0]

	@property
	def value(self):
		return self.additional[1]

	@property
	def value_node(self):
		''' Generates a node for self.value on the fly. '''
		if self.code == 1:
			return node.StringNode(self.value)
		elif self.code == 2:
			return node.MapNode()
		elif self.code == 3:
			return node.ListNode(self.value)
		elif self.code == 4:
			return node.NumberNode(self.value, self.additional[2])
		elif self.code == 5:
			return node.SingleNode()
		elif self.code == 6:
			return node.TrinaryNode(self.value)
		else:
			raise TypeError("Unknown instruction code, or does not have a value node")

	@property
	def deletions(self):
		result = []
		for i in self.additional:
			if type(i) == int:
				result.append((i,i))
			else:
				result.append(tuple(i))
		return result

def set(array):
	return [Instruction(x) for x in array]

def InsertText(address, pos, value):
	''' Accepts value type str or unicode '''
	return Instruction([1, address, pos, value])

def InsertMap(address, pos):
	''' Accepts list of sorted keys as value '''
	return Instruction([2, address, pos])

def InsertList(address, pos, value):
	''' Accepts list of descendant node keys as value '''
	return Instruction([3, address, pos, value])

def InsertNumber(address, pos, value, unique):
	''' Accepts list of sorted keys as value '''
	return Instruction([4, address, pos, value, unique])

def InsertSingle(address, pos):
	''' Accepts no value '''
	return Instruction([5, address, pos])

def InsertTrinary(address, pos, value):
	''' Accepts True, False, or None as value '''
	return Instruction([6, address, pos, value])

def InsertNode(address, pos, n):
	''' 
	Determines type of n and returns result of appropriate Insert* function.
	Does not insert children or handle deletions.
	'''

	if type(n) == node.StringNode:
		return InsertText(address, pos, n.value)
	elif type(n) == node.MapNode:
		return InsertMap(address, pos)
	elif type(n) == node.ListNode:
		return InsertList(address, pos, n.value)
	elif type(n) == node.NumberNode:
		return InsertNumber(address, pos, n.value, n.unique)
	elif type(n) == node.SingleNode:
		return InsertSingle(address, pos)
	elif type(n) == node.TrinaryNode:
		return InsertTrinary(address, pos, n.value)
	else:
		raise TypeError("Cannot create insertion instruction for type "+repr(type(n)))

def Delete(address, *positions):
	return Instruction([0, address]+list(positions))
