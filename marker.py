Default = {
	"style":{
		"emphasis":"False",
		"italic":"False"
	}, "link":{
		"resource":"False",
		"wave":"False"
	}, "meta":{
		"author":""
	}
}

class Marker:
	def __init__(self, category, subtype, value = None):
		self.category = category
		self.stype = subtype
		if value == None:
			self.value = Default[category][subtype]
		else:
			self.value = value

	@property
	def totaltype(self):
		return self.category +"/"+self.stype
