class Auth(object):
	''' Key-value store for storage spaces keyed on username. '''

	def __init__(self, storage_maker):
		self.maker = storage_maker
		self.contents = {}

	def load(self, username, password):
		" Add a user to cache from disk "
		if not username in self:
			self[username] = self.maker.make(username, password)

	def new(self, username, password, key=None):
		" Create a user "
		self[username] = self.maker.new(username, password, key)

	def __getitem__(self, username):
		return self.contents[username]

	def __setitem__(self, username, storage):
		self.contents[username] = storage

	def __delitem__(self, username):
		del self.contents[username]

	def __contains__(self, username):
		return username in self.contents
