'''
	Jack

	Base class for jacks. Each jack handles routing inbound and outbound
	for an address type, like UDP or Email.
'''

class Jack(object):
	def __init__(self, router):
		self.router = router

	def route(self, msg):
		# Send a message.Message from the router
		raise NotImplementedError("Subclasses of Jack must define route")

	def recv(self, data):
		# Send a string to the router (must be complete message)
		self.router.recv(data)
