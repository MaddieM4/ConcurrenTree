import hasher

Default = {
	"style":{
		"emphasis":False,
		"italic":False
	}, "link":{
		"resource":False,
		"wave":False
	}, "meta":{
		"author":""
	}
}

def sep(type):
	return tuple(type.split('/'))

class Marker:
	def __init__(self, category, subtype, 
			queue={}, ignore=[], applied=[], value=None):
		self.category = category
		self.stype = subtype
		self.value = value
		self.queue   = queue
		self.ignore  = ignore
		self.applied = applied

	def a_ignore(self, action):
		self.ignore.append(action.hash)

	def apply(self, action, recursive = True):
		if action.parent in self.ignore:
			self.a_ignore(action)
		if action.hash in self.ignore or action.hash in self.applied:
			return False
		r = False
		if action.parent in self.applied:
			pos = self.applied.index(action.parent)
			if pos == len(self.applied)-1:
				self.applied.append(action.hash)
				self.value = action.value
				r = True
			else:
				# deal with competition
				if self.applied[pos+1] < action.hash:
					# new action wins
					self.applied = self.applied[:pos]
					self.applied.append(action.hash)
					self.value = action.value
					r = True
				else:
					# new action loses
					self.a_ignore(action)
		else:
			self.queue[action.hash] = action
		if recursive:
			# work through queue
			retry = True
			while retry:
				retry = False
				for i in self.queue:
					retry = retry or self.apply(self.queue[i], False)
		return r

	@property
	def totaltype(self):
		return self.category +"/"+self.stype

	def action(self, value):
		if len(applied):
			return Action(value, applied[-1])
		else:
			return Action(value, "")

class Action:
	def __init__(self, value, parent):
		self.value = value
		self.parent = parent
		self.hash = hasher.make(self.value+self.parent)
		''' 
		if value == None:
			self.value = Default[category][subtype]
		else:
			self.value = value
		'''

	def apply(self, marker):
		marker.apply(self)
