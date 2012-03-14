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
		# Process in blocks
		value = str(value)
		result = []
		marker = 0
		totallen = len(value)
		while marker < totallen:
			result.append(self.key.encrypt(
				value[marker:marker+self.blocksize], "")[0])
			marker += self.blocksize
		return "".join(result)

	def decrypt(self, value):
		value = str(value)
		blocks = len(value) // 128
		result = []
		for i in range(blocks):
			s, e = i*128, i*128+128
			result.append(self.key.decrypt(value[s:e]))
		return "".join(result)

	@property
	def key(self):
		with self.genlock:
			return self._key

	@property
	def blocksize(self):
		# If you try to encrypt strings longer than the block size...
		# well, enjoy your heaping helping of useless gibberish.
		# This wrapper class handles blocking and deblocking for you.
		return self.key.size()/8-11 # May be overzealous, but better than not.

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
