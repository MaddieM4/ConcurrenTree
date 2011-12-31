import os.path
from ConcurrenTree.util.hasher import sum

class KeyFileOpener(object):
	def __init__(self, dir):
		self.dir = dir

	def get(self, username):
		filename = os.path.join(self.dir, sum(username))
		return open(filename, 'r').read()

	def set(self, username, value):
		filename = os.path.join(self.dir, sum(username))
		open(filename, 'w').write(value)
