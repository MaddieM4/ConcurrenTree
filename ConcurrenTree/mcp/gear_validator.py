import ConcurrenTree.validation as validation

class GearValidator(object):
	def __init__(self, gear):
		self.gear = gear
		self.queue = validation.ValidationQueue(filters = std_gear_filters)
		self.queue.gear = gear

	def validate(self, request):
		self.queue.filter(request)

	def pop(self):
		# Get the next item out of the queue
		return self.queue.pop()

	def op(self, author, docname, op):
		def callback(result):
			if result:
				self.gear.storage.op(docname, op)
			else:
				print "Rejecting operation for docname: %r" % docname
		self.validate(
			validation.make("operation", author, docname, op, callback)
		)

	def hello(self, author, encryptor):
		def callback(result):
			if result:
				self.gear.hosts.crypto_set(author, encryptor)
			else:
				print "Rejecting hello from sender: %r" % encryptor
		self.validate(
			validation.make("hello", author, encryptor, callback)
		)

# FILTERS

def filter_op_approve_all(queue, request):
	if isinstance(request, validation.OperationRequest):
		return request.approve()
	return request

def filter_op_is_doc_stored(queue, request):
	if isinstance(request, validation.OperationRequest):
		if not request.docname in queue.gear.storage:
			queue.gear.writer.error(request.author, message="Unsolicited op")
			return request.reject()
	return request

def filter_op_can_write(queue, request):
	if isinstance(request, validation.OperationRequest):
		if not queue.gear.can_write(request.author, request.docname):
			queue.gear.writer.error(request.author, message="You don't have write permissions.")
			return request.reject()
	return request

std_gear_filters = [
	filter_op_is_doc_stored,
	filter_op_can_write,
	filter_op_approve_all,
]
