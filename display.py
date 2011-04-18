class Display:
	''' 
		Base class for objects that communicate between the
		user and a CTree handler. Displays have a many-one
		relationship between documents - that is, you can
		have a document with no display, one, or even five
		displays, but you can never have multiple documents
		in one display. The display is an abstract object
		that may or may not plug directly into a graphical
		library, it's up to you.
	'''

	def replace(self, start, end, value):
		''' Replace part of the text content '''
		raise NotImplementedError("Subclasses of ConcurrenTree.display.Display must define self.replace(start, end, value)")

	def cursor(self, start, end):
		''' Set the cursor indexes '''
		raise NotImplementedError("Subclasses of ConcurrenTree.display.Display must define self.cursor(start, end)")

	def getcursor(self):
		''' Returns (start, end) of current cursor value '''
		raise NotImplementedError("Subclasses of ConcurrenTree.display.Display must define self.getcursor()")

	# TODO - marker functions
