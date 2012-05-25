from ejtp.util.crypto import make
import json

class CryptoFactory(object):
	''' Access to long-term storage of keys. '''
	def __init__(self, keystorage, locktype="aes"):
		self.keystorage = keystorage
		self.locktype = locktype
		self.passwdcache = {}

	def make(self, username, password):
		self.passwdcache[username] = password
		keystr = self.unlock(self.keystorage.get(username), password)
		return make(json.loads(keystr))

	def new(self, username, password, key=['rsa', None]):
		if self.keystorage.has(username):
			raise KeyError(str(username)+" already exists")
		self.passwdcache[username] = password
		key_obj = make(key)
		self.save(username, key_obj)
		return key_obj

	def save(self, username, key_obj):
		self.keystorage.set(username, self.lock(
			str(key_obj),
			self.passwdcache[username]
		))

	def delete(self, username):
		self.keystorage.delete(username)

	def unlock(self, keystr, password):
		return self.locker(password).decrypt(keystr)

	def lock(self, keystr, password):
		return self.locker(password).encrypt(keystr)

	def locker(self, password):
		return make([self.locktype, password])
