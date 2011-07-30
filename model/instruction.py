from address import Address
import hasher

def validpos(tree, pos):
	if not (pos <= len(tree) and pos >= 0):
		raise IndexError(pos, len(tree), "0 <= %d <= %d not true!" % (pos, len(tree)))

class Instruction:
	''' Base class for instructions. '''

	def apply(self, tree, address = None):
		''' Apply this instruction to a tree. Subclasses should override _apply (with the underline) instead. '''
		if not address and hasattr(self, 'address'):
			address = self.address
		if address:
			tree = Address(address).resolve(tree)
		self.sanitycheck(tree)
		self._apply(tree)

	def sanitycheck(self, tree):
		''' Check a tree to make sure this instruction can be applied. '''
		raise NotImplementedError("Subclasses of Instruction must define self.sanitycheck(tree)")

	def _apply(self, tree):
		''' Override this function in subclasses with code to operate on a tree. '''
		raise NotImplementedError("Subclasses of Instruction must define self._apply(tree)")

	def proto(self):
		''' Override this function in subclasses. '''
		raise NotImplementedError("Subclasses of Instruction must define self.proto()")

	@property
	def address_object(self):
		if hasattr(self, "address"):
			return Address(self.address)
		else:
			return Address([])

	@property
	def hash(self):
		return hasher.sum(str(self))

	def __str__(self):
		return hasher.strict(self.proto())

class Insertion(Instruction):
	''' Insert text into a tree. '''

	def __init__(self, address, position, value):
		self.address = address
		self.position = position
		self.value = value

	def sanitycheck(self, tree):
		validpos(tree, self.position)

	def _apply(self, tree):
		tree.insert(self.position, self.value)

	def proto(self):
		return [1, self.address.proto(), self.position, self.value]

class Deletion(Instruction):
	''' Delete text from a tree. '''

	def __init__(self, address, range):
		self.address = address
		if type(range)==int:
			self.range = [range, range]
		else:
			self.range = range

	def sanitycheck(self, tree):
		validpos(tree, self.range[0]) 
		validpos(tree, self.range[1]) 
		if self.range[1] < self.range[0]:
			raise ValueError(self.range[0], self.range[1], "%d should be >= %d" % (self.range[1], self.range[0]))

	def _apply(self, tree):
		for i in range(self.range[0], self.range[1]+1):
			tree.delete(i)

	def proto(self):
		if self.range[0]==self.range[1]:
			return [0, self.address.proto(), self.range[0]]
		else:
			return [0, self.address.proto(), self.range]

def set(array):
	result = []
	for i in array:
		result += deproto(i)
	return result

def deproto(instr):
	''' Returns a list of Instruction objects '''
	if isinstance(instr, Instruction):
		return [instr]
	address = instr[1]
	if instr[0]==0:
		# Deletion
		return [Deletion(address, i) for i in instr[2:]]
	else:
		# Insertion
		return [Insertion(address, instr[2], instr[3])]

# TODO - Marker instruction(s)
