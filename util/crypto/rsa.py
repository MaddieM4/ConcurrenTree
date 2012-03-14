import thread
import encryptor

from Crypto.PublicKey import RSA as rsalib

class RSA(encryptor.Encryptor):
	def __init__(self, keystr):
		self.keystr = keystr
		self._key = None
		self.genlock = thread.allocate()
		if keystr == None:
			self.genlock.acquire()
			self.generate()
		else:
			self._key = rsalib.importKey(keystr)

	def encrypt(self, value):
		return self.key.encrypt(str(value), "")[0] # No K value for RSA

	def decrypt(self, value):
		return self.key.decrypt(str(value))

	@property
	def key(self):
		with self.genlock:
			return self._key

	def generate(self, bits=1024):
		thread.start_new_thread(self._generate, (bits,))

	def _generate(self, bits):
		try:
			self._key = rsalib.generate(bits)
		finally:
			self.genlock.release()

	def proto(self):
		return ['rsa', self.key.exportKey()]

	def public(self):
		key = self.key.publickey()
		return ['rsa', key.exportKey()]
