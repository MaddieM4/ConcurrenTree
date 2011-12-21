from ConcurrenTree import file
import gtk
from gtk import gdk, StatusIcon

class Icon(StatusIcon):
	def __init__(self, server, logo=""):
		StatusIcon.__init__(self)
		self.set_from_file(file("img/logos/OrchardLogo%s.svg" % logo))
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
			gtk.SeparatorMenuItem(),
			self.item("Configure", self.server.configure, "gtk-preferences"),
			self.item("Manage Peers", self.server.info_peers, "gtk-redo"),
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
	def __init__(self, pool, logo=""):
		self.icon = Icon(self, logo)
		self._policy = Policy()
		self.properties = {}
		self.pool = pool
		self.closed = False

	def run(self):
		gdk.threads_init()
		gtk.main()

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
			"Peer address: "+ ("%s:%d" % poolprops['PeerServer']['address'])
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

	def info_peers(self, *args):
		dialog = gtk.MessageDialog()
		dialog.set_property("title", "Manage Peers")
		dialog.set_property("text", "Manage Peers")
		dialog.set_property("secondary-text", "When people connect to you, their port number will probably not be their host port.")
		listobj = PeerList({})
		dialog.vbox.pack_end(listobj.view)

		dialog.add_button("Refresh", 2)
		dialog.add_button("Connect", 3)
		dialog.add_button("Disconnect", 1)
		dialog.add_button("Done", 0)
		image = gtk.image_new_from_stock("gtk-network", gtk.ICON_SIZE_DIALOG)
		dialog.set_image(image)

		def update_peers():
			peerprops = self.pool.properties()['PeerServer']
			listobj.update(peerprops['connections'])

		def response(d, gint):
			if gint == 3:
				self.connect_to_peer()
				update_peers()
			if gint == 2:
				update_peers()
			elif gint == 1:
				selected = listobj.selected
				if selected != None:
					peerprops = self.pool.properties()['PeerServer']
					try:
						peerprops['disconnect'](listobj.selected)
					except KeyError:
						# No longer connected to that fileno anyways.
						pass
					update_peers()
			elif gint == 0:
				dialog.destroy()
		dialog.connect("response", response)
		dialog.show_all()
		update_peers()

	def connect_to_peer(self, *args):
		dialog = gtk.MessageDialog(buttons=gtk.BUTTONS_OK)
		dialog.set_property("title", "Orchard Connection Properties")		
		dialog.set_markup('Please enter the address of the Peer server:')

		def response(entry, dialog, r):
			dialog.response(r)

		entry = gtk.Entry()
		entry.connect("activate", response, dialog, gtk.RESPONSE_OK)

		hbox = gtk.HBox()
		hbox.pack_start(gtk.Label("Address:"), False, 5, 5)
		hbox.pack_end(entry)
		dialog.vbox.pack_end(hbox, True, True, 0)

		dialog.show_all()
		dialog.run()
		text = entry.get_text()
		dialog.destroy()

		peerserver = self.pool.properties()['PeerServer']
		peerserver['connect'](text)

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
		props['HTTP']['open'](url+"?ws="+str(wsport))

	def newwindow(self, *args):
		self.openwindow("/newclient")

	def opendocuments(self, *args):
		self.openwindow("/mydocuments")

	def configure(self, *args):
		self.openwindow("/facelift/settings")

class PeerList:
	def __init__(self, peers):
		self.view = gtk.TreeView()
		self.model = gtk.ListStore(int, str)
		self.columns = (
			(gtk.TreeViewColumn('Fileno'), gtk.CellRendererText(), 'text', 0), 
			(gtk.TreeViewColumn('Address'), gtk.CellRendererText(), 'text', 1)
		)

		for i in self.columns:
			self.view.append_column(i[0])
			i[0].pack_start(i[1], True)
			i[0].add_attribute(i[1], i[2], i[3])

		self.view.set_model(self.model)
		self.view.show_all()

		self.update(peers)

	def update(self, peers):
		self.peers = {}

		# Clear the ListStore
		while len(self.model) > 0:
			del self.model[0]

		# Repopulate
		for fileno in peers:
			peer = peers[fileno]
			self.peers[fileno] = self.model.append([fileno, peer.address])

	@property
	def selected(self):
		model, iter = self.view.get_selection().get_selected()
		if iter == None:
			return None
		fileno = int(model.get_value(iter, 0))
		return fileno

if __name__=="__main__":
	ike = Icon()
	main()
