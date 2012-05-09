
class ValidationRequest(object):
	def approve(self):
		self.callback(True)

	def reject(self):
		self.callback(False)
