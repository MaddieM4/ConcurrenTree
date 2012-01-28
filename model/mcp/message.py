'''
	Message

	Class for MCP messages.
'''

import json

class Message(object):
	def __init__(self, data):
		if type(data) in (str, unicode):
			data = str(data)
			self._load(data)
		elif type(data) == Message:
			self = Message

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

def make(type, addr, encryptor, content):
	straddr = json.dumps(addr)
	ciphercontent = encryptor.encrypt(content)
	msg = Message(type +straddr+'\x00'+ciphercontent)
	msg.content = content
	return msg
