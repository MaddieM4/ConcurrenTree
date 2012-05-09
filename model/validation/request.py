
class ValidationRequest(object):
	def callback(self, value):
		# Placeholder function to be overridden
		raise NotImplementedError("ValidationRequest callback was not overridden. Cannot call with value %r" % value)

	def approve(self):
		self.callback(True)

	def reject(self):
		self.callback(False)

	def __str__(self):
		return self.desc_string() + " " + repr(self.properties())

	def desc_string(self):
		return "Generic validation request."

	def properties(self):
		names = [x for x in dir(self) if not x.startswith('_')]
		results = {}
		for name in names:
			results[name] = getattr(self, name)
		return results
