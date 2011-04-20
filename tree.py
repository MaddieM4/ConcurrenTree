''' 
    Base class for all tree types, to ensure operations have reasonable 
    guarantees about what's available to use.
'''

class Tree:
	def insert(self, pos, value):
		''' Insert a child to the tree with string "value" at position "pos" '''
		raise NotImplmentedError("Subclasses of ConcurrenTree.tree.Tree must define self.insert(pos, value)")

	def delete(self, pos):
		''' Mark a character in a tree as deleted '''
		raise NotImplmentedError("Subclasses of ConcurrenTree.tree.Tree must define self.delete(pos)")

	def get(self, pos, hash):
		''' Return the subtree with hash "hash" from position "pos" '''
		raise NotImplmentedError("Subclasses of ConcurrenTree.tree.Tree must define self.get(pos, hash)")

	def mark(self, pos, marker):
		''' Set a marker on a position '''
		raise NotImplmentedError("Subclasses of ConcurrenTree.tree.Tree must define self.mark(pos, marker)")

	def __len__(self):
		''' Return the length of the internal immutable string '''
		raise NotImplmentedError("Subclasses of ConcurrenTree.tree.Tree must define self.__len__()")

	# The following are not necessary for Instructions, but are
	# nice, and may be relied upon by other stuff in the future

	def markers(self):
		''' 
		Returns a dict (keyed on position) of dict[totaltype] = marker.
		'''
		raise NotImplmentedError("Subclasses of ConcurrenTree.tree.Tree should define self.markers()")

	def children(self):
		''' 
		Returns a dict (keyed on position) of sorted child hash lists.
		'''
		raise NotImplmentedError("Subclasses of ConcurrenTree.tree.Tree should define self.children()")

	def flatten(self):
		''' 
		Returns a single-level tree that is display-equivalent to self.
		'''
		raise NotImplmentedError("Subclasses of ConcurrenTree.tree.Tree should define self.flatten()")

	def trace(self, pos):
		''' 
		Given a position in the flat text, compute an (address, position) pair.
		'''
		raise NotImplmentedError("Subclasses of ConcurrenTree.tree.Tree should define self.flatten()")
