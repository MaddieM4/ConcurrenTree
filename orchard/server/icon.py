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
		self.connect("popup-menu", self.rightclick)

	def leftclick(self, icon):
		self.menu(1, gtk.get_current_event_time(), self.litems())

	def rightclick(self, data, event_button, event_time):
		self.menu(event_button, event_time, self.ritems())

	def menu(self, event_button, event_time, items):
		menu = gtk.Menu()
		for item in items:
			if type(item)==str:
				item = gtk.MenuItem(item)
			menu.append(item)
			item.show_all()
		menu.show_all()
		menu.popup(None, None, gtk.status_icon_position_menu, event_button, event_time, self)

	def litems(self):
		return [
			"Future",
			"feature:",
			"a list",
			"of documents",
			"here.",
			self.item("New Document", self.server.newwindow, "gtk-add"),
			gtk.SeparatorMenuItem(),
			self.item("gtk-about", self.server.about),
			self.item("gtk-quit", self.server.quit)
		]


	def ritems(self):
		return [
			self.item("New Window", self.server.newwindow, "gtk-add"),
			self.item("My Documents", self.server.opendocuments, "gtk-home"),
			self.item("Connection Information", self.server.info, "gtk-network"),
			self.item("Connect to peer", self.server.info, "gtk-network"),
			gtk.SeparatorMenuItem(),
			self.item("Configure", self.server.configure, "gtk-preferences"),
			gtk.SeparatorMenuItem(),
			self.item("gtk-about", self.server.about),
			self.item("gtk-quit", self.server.quit)
		]

	def item(self, name, function, image=""):
		item = gtk.ImageMenuItem(name)
		item.set_use_stock(True)
		if image:
			item.set_image(gtk.image_new_from_stock(image,gtk.ICON_SIZE_MENU))
		item.connect("activate", function)
		return item

class IconServer(Server):
	def __init__(self, pool):
		self.icon = Icon(self)
		self._policy = Policy()
		self.properties = {}
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

	# functions for internal icon to call

	def quit(self, *args):
		self.pool.close_signal()

	def info(self, *args):
		dialog = gtk.MessageDialog()
		dialog.set_property("title", "Orchard Connection Properties")
		dialog.set_property("text", "Orchard Connection Properties")
		poolprops = self.pool.properties()
		properties = [
			"HTTP port: "+str(poolprops['HTTP']['port']),
			"WebSocket port: "+str(poolprops['WebSocket']['port']),
			"Peer address: "+str(poolprops['PeerServer']['address'])
		]
		dialog.set_property("secondary-text", "\n".join(properties))
		#dialog.set_property("use-markup", True)
		dialog.add_button("Done", 0)
		image = gtk.image_new_from_stock("gtk-network", gtk.ICON_SIZE_DIALOG)
		dialog.set_image(image)
		def response(d, gint):
			d.destroy()
		dialog.connect("response", response)
		dialog.show_all()

	def about(self, *args):
		dialog = gtk.AboutDialog()
		dialog.set_program_name("Orchard")
		dialog.set_version("0.3")
		dialog.set_website("http://github.com/campadrenalin/ConcurrenTree")
		dialog.set_website_label("ConcurrenTree library on Github")
		dialog.set_comments("""Orchard is an implementation of the evolving concurrent text standard, ConcurrenTree. It's 
		under active development right now, expect broken pieces and jagged edges.
		""".replace("\t","").replace('\n', ''))
		dialog.set_authors(["Philip Horger <campadrenalin@gmail.com>","Nathaniel Abbots"])
		dialog.set_logo(gtk.gdk.pixbuf_new_from_file(file("img/logos/OrchardBigLogo.svg")))
		def response(d, gint):
			d.destroy()
		dialog.connect("response", response)
		dialog.show()

	def openwindow(self, url):
		props = self.pool.properties()
		wsport = props['WebSocket']['port']
		props['HTTP']['open'](url+"#ws="+str(wsport))

	def newwindow(self, *args):
		self.openwindow("/newclient")

	def opendocuments(self, *args):
		self.openwindow("/mydocuments")

	def configure(self, *args):
		# TODO - Make a Configuration dialog.
		pass

if __name__=="__main__":
	ike = Icon()
	main()
