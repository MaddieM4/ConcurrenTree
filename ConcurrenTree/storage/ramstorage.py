from ConcurrenTree.storage import BaseStorage

class RAMStorage(BaseStorage):
	# Minimalist storage class

	def __init__(self, find=None, encryptor=None):
		BaseStorage.__init__(self, find=find, encryptor=encryptor)
		self.cache = {}

	def get(self, i):
		return self.cache[i]

	def set(self, i, v):
		self.cache[i] = v

	def has(self, i):
		return i in self.cache

	def delete(self, i):
		del self.cache[i]

	def flush(self):
		pass

	def uncache(self, i):
		del self[i]

class RAMStorageFactory(object):
	def __init__(self, find=None, encryptorFactory=None):
		pass

	def make(self, username, password):
		# Ignore both
		return RAMStorage()
