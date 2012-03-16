import node
import single
from ConcurrenTree.util import hasher

class MapNode(node.Node):
	def __init__(self, limit={}, source={}):
		node.Node.__init__(self)
		self._value = limit
		self._data = {}
		for k in self.value:
			if isinstance(self.value[k], node.Node):
				self._value[k] = self.value[k].key
			print "Setting limit on", k
			s = single.SingleNode(limit=self.value[k])
			self[k] = s
		self.update(source)

	def update(self, source):
		# Items must already be nodes
		for k in source:
			s = single.SingleNode()
			s.put(0, source[k])
			self[k] = s

	@property
	def value(self):
		return self._value

	@property
	def key(self):
		return self.keysum(hasher.strict(self.value))

	def flatten(self):
		result = {}
		for i in self._data:
			result[i] = self._data[i].flatten()
			if result[i] == None:
				del result[i]
		return result

	def _get(self, pos, key):
		# Due to mapping semantics, "pos" is the key, and "key" must be "/single".
		if key != "/single":
			raise KeyError("Mapping can only contain SingleNodes")
		if type(pos) not in (unicode, str):
			raise TypeError("pos must be str")
		return self._data[pos]

	def _put(self, pos, obj):
		# "pos" should be a string key.
		if type(pos) not in (unicode, str):
			raise TypeError("pos must be str, got %r instead" % pos)
		if not isinstance(obj,single.SingleNode):
			raise TypeError("obj must be a SingleNode")
		self._data[pos] = obj

	def _delete(self, pos):
		raise node.Undelable()

	@property
	def children(self):
		result = {}
		for k in self:
			result[k] = {"/single":self[k].hash}
		return result

	@property
	def deletions(self):
		return []

	def resolve(self, addrlist):
		if len(addrlist) == 0:
			return self
		else:
			return self.get(addrlist[0],addrlist[1]).resolve(addrlist[2:])

	# Plumbing

	def __iter__(self):
		return self._data.__iter__()

	def __getitem__(self, key):
		return self.get(key, "/single")

	def __setitem__(self, key, obj):
		self.put(key, obj)
