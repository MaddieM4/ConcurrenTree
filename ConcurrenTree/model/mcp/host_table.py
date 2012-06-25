from ejtp.address import *

class HostTable(object):
	def __init__(self, document=None):
		'''
		Convenience wrapper for host resolution tables.

		>>> hosty = HostTable()
		>>> hosty.document #doctest: +ELLIPSIS
		<ConcurrenTree.model.document.Document object at ...>
		>>> hosty.wrapper
		w<{'content': {}, 'routing': {}}>

		'''
		if document == None:
			from ConcurrenTree.model.document import Document
			document = Document()
		self.document = document
		self.wrapper = self.document.wrapper()

	# Access --------------------------------------------------------------

	def __getitem__(self, k):
		return self.wrapper['content'][k]

	def __setitem__(self, k, i):
		self.wrapper['content'][k] = i

	def __delitem__(self, i):
		del self.wrapper['content'][k]

	def __contains__(self, k):
		k = str_address(k)
		return k in self.wrapper['content']

	def get(self, address):
		'''
		Ensures that address is in string form, before returning
		the host data from the table.

		>>> hosty = HostTable()
		>>> addr = ['vaporware', ['bob'], 'catalina']
		>>> addr in hosty
		False
		>>> hosty.get(addr)
		w<{}>
		>>> addr in hosty
		True
		>>> hosty.set(addr, {'vikings':'pillagers'})
		>>> hosty.get(addr)
		w<{'vikings': 'pillagers'}>
		>>> addr in hosty
		True
		''' 
		address = str_address(address)
		if not address in self:
			self.set(address, {})
		return self[address]

	def set(self, address, i):
		'''
		Sets the data in the host document for a specific address.
		'''
		address = str_address(address)
		self[address] = i

	# Cryptography --------------------------------------------------------

	def crypto_set(self, iface, proto):
		'''
		Set encryptor information for an interface address.

		>>> hosty = HostTable()
		>>> addr = ['vaporware', ['bob'], 'catalina']
		>>> hosty.crypto_get(addr)
		Traceback (most recent call last):
		KeyError: 'encryptor'
		>>> hosty.crypto_set(addr, ['whalecipher', 'awooga'])
		>>> hosty.crypto_get(addr)
		['whalecipher', 'awooga']
		'''
		self.get(iface)['encryptor'] = [proto, []]

	def crypto_get(self, iface):
		return self.get(iface)['encryptor'].value[0]
