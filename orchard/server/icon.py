from server import *

from ConcurrenTree import file
import gtk
from gtk import gdk, StatusIcon

class Icon(StatusIcon):
	def __init__(self, server):
		StatusIcon.__init__(self)
		self.set_from_file(file("img/logos/OrchardLogo.svg"))
		self.set_tooltip("Orchard Server")
		self.server = server
		self.connect("activate", self.leftclick)

	def leftclick(self, icon):
		self.menu(1, gtk.get_current_event_time(), self.litems())

	def menu(self, event_button, event_time, items):
		menu = gtk.Menu()
		for item in items:
			if type(item)==str:
				item = gtk.MenuItem(item)
			menu.append(item)
			item.show()
		menu.show()
		menu.popup(None, None, gtk.status_icon_position_menu, event_button, event_time, self)

	def litems(self):
		return [
			"New Window",
			"My Documents",
			"Connection Information",
			self.item("Quit", lambda x: self.server.pool.close_signal())
		]

	def item(self, name, function):
		item = gtk.MenuItem(name)
		item.connect("activate", function)
		return item

class IconServer(PoolServer):
	def __init__(self, pool):
		self.icon = Icon(self)
		self._policy = Policy()
		self.pool = pool
		self.closed = False

	def run(self):
		gdk.threads_init()
		gtk.main()

	def starting(self):
		return []

	def policy(self):
		return self._policy

	def close(self):
		self.closed = True
		gtk.main_quit()

if __name__=="__main__":
	ike = Icon()
	main()
