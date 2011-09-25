from ConcurrenTree.model import ModelBase
import re
import json

class Address(ModelBase):
	''' Address format: [[index, key], [index, key]] '''

	def __init__(self, target):
		if type(target)==list:
			self.parse(target)
		elif isinstance(target, Address):
			self.layers = target.layers
		elif type(target) in (str, unicode):
			self.layers = json.loads(target)
		else:
			raise TypeError("Expected list or address.Address, got "+str(type(target)))

	def parse(self, l):
		''' Does not check for syntax errors yet '''
		self.layers = []
		pos = None
		for i in l:
			if type(i)==int:
				pos = i
			else:
				if pos==None:
					self.layers.append(i)
				else:
					self.layers.append((pos,i))
					pos = None

	def resolve(self, tree):
		x = tree
		for i in self.layers:
			if type(i) in (str, unicode):
				i = (len(x), i)
			x = x.get(i[0],i[1])
		return x

	def proto(self):
		result = []
		for i in self.layers:
			if type(i)==tuple:
				result += list(i)
			else:
				result.append(i)
		return result
