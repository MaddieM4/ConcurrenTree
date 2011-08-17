# An older implementation of eras used the classes below.
# I tore most of the code out but this part was too good
# and took too much work, so I'm keeping it for now on
# the remote chance we need it again, so I won't have to
# recode it again. ~ Philip

class TreeReference(dict):
	''' 
		An object that acts as a proxy for an actual tree,
		using an era to request the tree on the fly. Treat it
		like a regular old Tree object, but be forewarned that
		those functions may raise ShortcutUnresolvedErrors if
		the era can't resolve the shortcut to a Tree.
	'''
	def __init__(self, era, shortcut, tree=None):
		super(TreeReference, self).__init__()
		self.era = era
		self.shortcut = validate_shortcut(shortcut)
		if tree!=None:
			self.set(tree)

	def __getattr__(self, attr):
		if attr in dir(Tree):
			return getattr(self.tree, attr)
		else:
			if attr in self:
				return self[attr]
			else:
				raise AttributeError(attr)

	def __setattr__(self, attr, value):
		if attr in dir(Tree):
			setattr(self.tree, attr, value)
		else:
			self[attr] = value

	def __repr__(self):
		return "<tree.TreeReference instance: %s>" % str(self.shortcut)

	def proto(self):
		return {"address":["#"+str(self.shortcut[0]), self.shortcut[1]]}

	@property
	def tree(self):
		return self.era.resolve(self.shortcut)

	def set(self, tree):
		self.era.insert(self.shortcut, tree)
