'''
	Message

	Class for MCP messages.
'''

from ConcurrenTree.util import hasher
import json

PACKET_SIZE = 8192

class Message(object):
	def __init__(self, data):
		if type(data) in (str, unicode, Message):
			data = str(data)
			self._load(data)

	def _load(self, data):
		self.type = data[0]
		sep = data.index('\x00')
		self.straddr = data[1:sep]
		self.ciphercontent = data[sep+1:]
		self.addr = json.loads(self.straddr)
		if (type(self.addr) != list or len(self.addr)<3):
			raise ValueError("Bad address: "+repr(self.addr))

	def __str__(self):
		return self.type+self.straddr+'\x00'+self.ciphercontent

	def decode(self, encryptor):
		if not self.decoded:
			self.content = encryptor.decrypt(self.ciphercontent)
		return self.content

	@property
	def decoded(self):
		return hasattr(self, "content")

def onion(msg, hops=[]):
	'''
		Encrypt a message into multiple hops, splitting the end
		result into a multihop if necessary.

		To split into multipart with only one recipient, call
		with the plaintext as "msg" and only one (addr, encryptor)
		tuple in "hops".
	'''
	for (addr, encryptor) in hops:
		msg = make('r', addr, encryptor, str(msg))
	if len(msg) > PACKET_SIZE:
		# Split into multiple parts
		straddr = msg[1:msg.index('\x00')]
		addrlen = len(straddr)
		chunksize = PACKET_SIZE-(2+addrlen)

		chunks = split_text(msg, chunksize)
		hashes = [hasher.make(c) for c in chunks]

		mpmsg = hasher.strict({
			'type':'multipart',
			'parts':hashes,
			'id':hasher.make(msg)
		})
		multipart = onion(mpmsg, hops[-1:])
		return multipart + ["r"+straddr+'\x00'+c for c in chunks]
	else:
		return [msg]

def make(type, addr, encryptor, content):
	straddr = hasher.strict(addr)
	ciphercontent = encryptor.encrypt(content)
	msg = Message(type +straddr+'\x00'+ciphercontent)
	msg.content = content
	return msg

def split_text(txt, size):
	# Split txt into an array of chunks, "size" or smaller
	if size <= 0:
		raise ValueError("Chunk size must be > 0, was given "+repr(size))
	marker = 0
	total = len(txt)
	result = []
	while marker < total:
		result.append(txt[marker:marker+size])
		marker += size
	return result
