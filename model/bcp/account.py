import os.path
from ConcurrenTree.util import hasher
from ConcurrenTree.util.storage.filestorage import FileStorage

ACCOUNT_DIR = os.path.join("~/", '.ConcurrenTree', 'accounts')

class Account(object):
	def __init__(self, username, password, dir = ACCOUNT_DIR):
		self.key = self.load(username, password)
		self.storage = FileStorage(dir = os.path.join(dir, "storage"))

	def load(self, username, password=None):
		if password == None:
			return self.load_key(username)
		else:
			# Load and decrypt pair
			pair = self.load(username)
			return pair

	def load_key(self, username):
		raise NotImplementedError("Account.load_key is left for subclasses to define")
