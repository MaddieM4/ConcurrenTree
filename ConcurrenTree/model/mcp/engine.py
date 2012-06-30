from gear import Gear

class Engine(object):
	# Produces gears

	def __init__(self, auth=None, router=None):
		self.auth = auth or default_auth()
		self.router = router or default_router()

	def make(self, username, password, interface, **kwargs):
		return self.gear(self.auth.make(username, password), interface, **kwargs)

	def gear(self, storage, interface, **kwargs):
		return Gear(storage, self.router, interface, **kwargs)

def default_auth():
	from ConcurrenTree.model.auth import Auth
	return Auth()

def default_router():
	from ejtp import router
	return router.Router()
