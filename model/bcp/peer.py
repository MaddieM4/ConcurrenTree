class Peer:
	''' Represents a remote endpoint. '''
	def __init__(self):
		self.selected = None
		self.subscriptions = set()
		self.ops = set()
