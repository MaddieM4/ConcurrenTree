class Context(object):
	# Base class for all context objects, defines API
	def __init__(self, node):
		self.node = node
		self.register()
		self.live = Live(self)

	@property
	def value(self):
		return self.node.flatten()

	def register(self):
		# Register with node callbacks
		pass

class Live(object):
	# Applies context actions directly
	# For example, mycontext.live.insert(4, "Mayweather") does not just return
	# an op, it also applies it first.
	def __init__(self, context):
		self.context = context

	def __getattribute__(self, name):
		if name == "context":
			return object.__getattribute__(self, name)
		else:
			func = object.__getattribute__(self.context, name)
			def wrap_live(*args, **kwargs):
				op = func(*args, **kwargs)
				self.context.node.apply(op)
				return op
			return wrap_live
