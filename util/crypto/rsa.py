from Crypto.PublicKey import RSA
from aes import AESUnlocker

class RSA(object):
	def __init__(self, keystr, password):
		self.keystr = keystr
		self.key = self.unlock(keystr, password)

	def encrypt(self, value):
		return self.key.encrypt(value)

	def decrypt(self, value):
		return self.key.decrypt(value)

	def unlock(self, keystr, passwd):
		return RSA.importKey(AESUnlocker(passwd).decrypt(keystr))

	def lock(self, passwd):
		return AESUnlocker(passwd).encrypt(self.key.exportKey())
