class CryptoFactory(object):
	def __init__(self, keystorage, unlocker):
		self.keystorage = keystorage
		self.unlocker = unlocker

	def make(self, username, password):
		key = self.keystorage.get(username)
		return self.unlocker(key, password)
