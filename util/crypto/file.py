import os.path
from ConcurrenTree.util.hasher import sum

class KeyFileOpener(object):
	def __init__(self, dir):
		import os.path
		self.dir = os.path.expanduser(dir)
		if not os.path.exists(self.dir):
			import os
			os.makedirs(self.dir)
			print "Creating dir:", repr(self.dir)

	def get(self, username):
		if not self.has(username):
			raise KeyError(username)
		return open(self.filename(username), 'r').read()

	def set(self, username, value):
		open(self.filename(username), 'w').write(value)

	def has(self, username):
		return os.path.exists(self.filename(username))

	def delete(self, username):
		import os
		os.remove(self.filename(username))

	def filename(self, username):
		return os.path.join(self.dir, sum(username))
