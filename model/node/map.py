import node

class MapNode(node.Node):
	def __init__(self, keys=[], source={}):
		self._value = list(set(keys).union(set(source.keys()))) # unique all the keys
		self._value = [str(x) for x in self.value] # convert them to strings
		self._value.sort()
		self._length = len(self._value)
		self._children = [node.ChildSet() for i in range(0, len(self))]
		self._deletions = [False for i in range(0, len(self))]
		self.extension = node.ChildSet(MapNode)

	# Node interface

	@property
	def value(self):
		return self._value

	@property
	def key(self):
		return self.keysum("{%s}" % ",".join(self.value))

	def flatten(self, existing = {}):
		result = existing
		for k in self:
			i = self.index(k)
			if self._deletions[i]:
				del result[k]
			else:
				obj = self[k]
				if obj!=None:
					obj = obj.flatten()
				result[k] = obj
		for i in self.extension.values:
			result = i.flatten(result)
		return result

	def get(self, pos, key):
		if type(pos) != int:
			raise TypeError("pos must be an int")
		if type(key) != str:
			raise TypeError("key must be a str")
		if pos == len(self):
			return self.extension[key]
		else:
			return self._children[pos][key]

	def put(self, pos, obj):
		if type(pos) != int:
			raise TypeError("pos must be an int")
		if not isinstance(obj,node.Node):
			raise TypeError("obj must be a subclass of Node")
		if pos == len(self):
			self.extension.insert(obj)
		else:
			self._children[pos].insert(obj)

	def delete(self, pos):
		self._deletions[pos] = True

	def proto(self):
		pass #TODO - figure out protocol representation for advanced types

	# Operations - all functions in this section return Operation objects

	def extend(self, values={}):
		''' Equivalent to dict.update, creating children as necessary '''
		if len(self.extension)==0:
			pass

	# Plumbing

	def index(self, key):
		return self.value.index(key)

	def __len__(self):
		return self._length

	def __iter__(self):
		return self.value.__iter__()

	def __getitem__(self, key):
		try:
			return self._children[self.index(key)].head
		except ValueError:
			raise KeyError("Key %s not present in MapNode" % repr(key))
		except IndexError:
			return None

	def __setitem__(self, key, obj):
		self.put(self.index(key), obj)
