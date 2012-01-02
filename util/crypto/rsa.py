from Crypto.PublicKey import RSA as rsalib
from aes import AESUnlocker

class RSA(object):
	def __init__(self, keystr, password):
		self.keystr = keystr
		self.password = password
		if keystr == None:
			self.generate()
		else:
			self.unlock()

	def encrypt(self, value):
		return self.key.encrypt(value, "")[0] # No K value for RSA

	def decrypt(self, value):
		return self.key.decrypt(value)

	def unlock(self):
		self.key = rsalib.importKey(AESUnlocker(self.password).decrypt(self.keystr))

	def lock(self):
		return AESUnlocker(self.password).encrypt(self.key.exportKey())

	def generate(self, bits=1024):
		# TODO - move to external process so that CPU-bound
		# generation does not freeze greenlet reactor loop
		self.key = rsalib.generate(bits)
