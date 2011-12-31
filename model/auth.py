class Auth(object):
	''' Key-value store for storage spaces keyed on username. '''

	def __init__(storage_maker):
		self.maker = storage_maker
		self.contents = {}

	def load(self, username, password):
		if not username in self:
			self[username] = storage_maker(username, password)

	def __getitem__(self, username):
		return self.contents[username]

	def __setitem__(self, username, storage):
		self.contents[username] = storage

	def __delitem__(self, username):
		del self.contents[username]
