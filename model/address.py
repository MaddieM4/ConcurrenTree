from ConcurrenTree.model import ModelBase
import re
import json

class Address(ModelBase):
	''' Address format: [[index, key], [index, key]] '''

	def __init__(self, target):
		self.layers = []
		if type(target)==list:
			self.layers = target
		elif isinstance(target, Address):
			self.layers = target.layers
		elif type(target)==str:
			self.layers = json.loads(target)
		else:
			raise TypeError("Expected list or address.Address, got "+str(type(target)))

	def resolve(self, tree):
		x = tree
		for i in self.layers:
			x = x.get(i[0],i[1])
		return x

	def proto(self):
		return self.layers
