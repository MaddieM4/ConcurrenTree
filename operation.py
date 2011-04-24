import instruction
import hasher
from address import Address
from copy import deepcopy

class Operation:
	''' A collection of instructions '''

	def __init__(self, instructions = [], protostring = None):
		''' If protostring is present, uses that existing protocol object. If not, use instructions list. '''
		if protostring:
			# process protostring
			pass
		else:
			self.instructions = instructions

	def apply(self, tree):
		backup = deepcopy(tree)
		for i in self.instructions:
			try:
				i.apply(tree)
			except Exception as e:
				tree = backup
				raise e

	@property
	def inserts(self):
		results = []
		for i in self.instructions:
			if isinstance(i,instruction.Insertion):
				results.append(i)
		return results

	@property
	def dep_provides(self):
		''' The dependencies that this operation provides to the tree '''
		return set([str(i.address_object)+str(i.position)+":"+hasher.make(i.value) for i in self.inserts])

	@property
	def dep_requires(self):
		''' The dependencies that this operation requires before it can be applied '''
		return set([str(i.address_object) for i in self.instructions]) - self.dep_provides

	def ready(self, tree):
		''' Checks a tree for existence of all dependencies '''
		for i in self.dep_requires:
			try:
				Address(i).resolve(tree)
			except Exception as e:
				print e
				return False
		return True

	@property
	def hash(self):
		return hasher.make(str(self))

	def __str__(self):
		''' Returns a protocol operation object '''
		return ""