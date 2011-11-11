from ConcurrenTree.model import ModelBase, node
import ConcurrenTree.util.hasher as hasher
import instruction
from address import Address
from copy import deepcopy
import traceback
import json

class Operation(ModelBase):
	''' A collection of instructions '''

	def __init__(self, instructions = [], protostring = None):
		''' If protostring is present, uses that existing serialized instruction set. If not, use instructions. '''
		if type(instructions) == Operation:
			self.instructions = list(instructions.instructions)
		else:
			if protostring:
				instructions += json.loads(protostring)
			try:
				self.instructions = instruction.set(instructions)
			except:
				raise ParseError()

	def apply(self, tree):
		#self.sanitycheck(tree)

		if not isinstance(tree, node.Node):
			return tree.apply(self)

		backup = deepcopy(tree)
		for i in self.instructions:
			try:
				i.apply(tree)
			except Exception as e:
				tree = backup
				traceback.print_exc()
				raise OpApplyError()

	def prefix(self, addr):
		''' Prepend all instruction addresses with addr '''
		for i in self.instructions:
			i.address = addr + i.address

	@property
	def inserts(self):
		results = []
		for i in self.instructions:
			if i.isinsert:
				results.append(i)
		return results

	@property
	def dep_provides(self):
		''' The dependencies that this operation provides to the tree '''
		return set([str(i.address.proto()+[i.position, i.value]) for i in self.inserts])

	@property
	def dep_requires(self):
		''' The dependencies that this operation requires before it can be applied '''
		return set([str(i.address) for i in self.instructions]) - self.dep_provides

	def ready(self, tree):
		''' Checks a tree for existence of all dependencies '''
		for i in self.dep_requires:
			try:
				Address(i).resolve(tree)
			except Exception as e:
				traceback.print_exc()
				return False
		return True

	def sanitycheck(self, tree):
		if not self.ready(tree): return False

	def applied(self, tree):
		''' Returns whether or not this op has been applied to the tree '''
		if hasattr(tree, "applied"):
			return self.hash in tree.applied
		else:
			return False

	def compress(self):
		# Todo - op compression (combining deletion instructions together)
		pass

	def proto(self):
		''' Returns a protocol operation object '''
		return {"type":"op","instructions":[i.proto() for i in self.instructions]}

	# Plumbing

	def __len__(self):
		return len(self.instructions)

	def __add__(self, other):
		new = Operation(self)
		new += other
		return new

	def __radd__(self, other):
		# Instruction
		if isinstance(other, instruction.Instruction):
			self.instructions = [other] + self.instructions

		# Address
		elif isinstance(other, Address):
			self.prefix(other)		

	def __iadd__(self, other):
		# Operation
		if isinstance(other, Operation):
			self.instructions += other.instructions

		# Instruction
		elif isinstance(other, instruction.Instruction):
			self.instructions.append(other)

		# Address
		elif isinstance(other, Address):
			self.prefix(other)

		return self

def FromChildren(n):
	''' Creates an op for the descendants of n with the assumption that n is root '''
	op = Operation()

	children = n.children
	if children != None:
		for i in range(len(children)):
			child = children[i]
			for k in child:
				op += FromNode(child[k], i)
	return op

def FromNode(n, pos):
	''' Converts node n into an op that inserts it and its descendants to root '''

	op = Operation([instruction.InsertNode([], pos, n)])
	addr = Address([pos, n.key])

	deletions = n.deletions
	if deletions != []:
		op += instruction.Delete(addr, *deletions)

	op += FromChildren(n) + addr

	return op

def FromStructure(root, address=[]):
	''' Returns an op that inserts the node at address (and its descendants) to root '''
	address = Address(address)

	if len(address) > 0:
		pos = address.position(root)
		return FromNode(address.resolve(root), pos) + address.parent
	else:
		return FromChildren(root)

class ParseError(SyntaxError): pass
class OpApplyError(SyntaxError): pass
