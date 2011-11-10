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

def FromNode(n, pos):
	''' Turns node n into an operation that inserts into root at position pos '''
	op = Operation([instruction.InsertNode([], pos, n)])
	addr = Address([pos, n.key])

	deletions = n.deletions
	if deletions != []:
		op += instruction.Delete(addr, *deletions)

	children = n.children
	if children != None:
		for i in range(len(children)):
			print "Childset ",i
			child = children[i]
			for k in child:
				print "\tkey:", repr(k)
				print "\tchild:", repr(child[k])
				childop = FromNode(child[k], i) + addr
				print "\tchildop:", childop.instructions
				op += childop
	return op

class ParseError(SyntaxError): pass
class OpApplyError(SyntaxError): pass
