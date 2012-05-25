from gear import Gear
from ejtp.client import Client

class Engine(object):
	# Produces gears

	def __init__(self, auth=None, router=None, mkclient = Client):
		self.auth = auth or default_auth()
		self.router = router or default_router()
		self.mkclient = mkclient

	def make(self, username, password):
		# Fail if it does not exist yet
		self.auth.load(username, password)
		return self.gear(self.auth[username])

	def new(self, username, password):
		# Succeed as long as user doesn't already exist with different password
		self.auth.new(username, password)
		return self.gear(self.auth[username])

	def validate(self, username, password):
		# Test login pair
		return self.auth.verify(username, password)

	def gear(self, storage):
		return Gear(storage, self.router, self.mkclient)

def default_auth():
	from ConcurrenTree.storage.default import DefaultAuth
	return DefaultAuth()

def default_router():
	from ejtp import router
	return router.Router()
