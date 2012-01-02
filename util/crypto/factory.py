class CryptoFactory(object):
	def __init__(self, keystorage, keyclass):
		self.keystorage = keystorage
		self.keyclass = keyclass

	def make(self, username, password):
		keystr = self.keystorage.get(username)
		return self.keyclass(keystr, password)

	def new(self, username, password, key=None):
		key_obj = self.keyclass(key, password)
		self.save(username, key_obj)
		return key_obj

	def save(self, username, key_obj):
		self.keystorage.set(username, key_obj.lock())
