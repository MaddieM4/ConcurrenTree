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
		filename = os.path.join(self.dir, sum(username))
		return open(filename, 'r').read()

	def set(self, username, value):
		filename = os.path.join(self.dir, sum(username))
		open(filename, 'w').write(value)
