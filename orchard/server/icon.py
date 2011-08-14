from server import *

from ConcurrenTree import file
from gtk import gdk, StatusIcon, main, main_quit

class Icon(StatusIcon):
	def __init__(self, server):
		StatusIcon.__init__(self)
		self.set_from_file(file("img/logos/OrchardLogo.svg"))
		self.set_tooltip("Orchard Server")
		self.server = server

class IconServer(PoolServer):
	def __init__(self):
		self.icon = Icon(self)
		self._policy = Policy()
		self.closed = False

	def run(self):
		gdk.threads_init()
		main()

	def starting(self):
		return []

	def policy(self):
		return self._policy

	def close(self):
		self.closed = True
		main_quit()

if __name__=="__main__":
	ike = Icon()
	main()
