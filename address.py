import re

class Address:
	''' Address format: index:hash/index:hash '''

	def __init__(self, target):
		self.layers = []
		if type(target)==list:
			self.layers = target
		elif type(target) == Address:
			self.layers = target.layers
		else:
			raise TypeError("Expected list or address.Address, got "+str(type(target)))

	def resolve(self, tree):
		x = tree
		for i in self.layers:
			x = x.get(i[0],i[1])
		return x

	def __str__(self):
		return '[%s]' % ",".join(["[%d,%s]" % i for i in self.layers])
