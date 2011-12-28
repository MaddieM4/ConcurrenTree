# Core handlers

from ConcurrenTree.model import operation, address

def select(self, obj, objstring, type):
	if not self.require("docname", obj): return
	self.there.selected = obj['docname']

def op(self, obj, objstring, type):
	if not self.check_selected():return
	if not self.require("instructions", obj): return
	try:
		op = operation.Operation(instructions = obj['instructions'])
	except operation.ParseError:
		return self.error(453)
	# TODO: authorize
	if not op.applied(self.fdoc):
		try:
			op.apply(self.fdoc)
			print "Tree '%s' modified: '%s'" % (self.there.selected, self.fdoc.flatten())
			print "New hash: '%s'" % self.fdoc.hash
			self.pool_push({
				"type":"op",
				"docname":self.there.selected,
				"value":op
			})
		except operation.OpApplyError:
			self.error(500) # General Local Error
	else:
		print "Op was already applied"

def get(self, obj, objstring, type):
	if not self.check_selected():return
	if not self.require("address", obj):return
	self.sendop(self.there.selected, obj['address'])

def check(self, obj, objstring, type):
	# TODO - error testing
	if not self.check_selected():return
	if not self.require("address", obj):return
	addr = address.Address(obj['address'])
	sum = addr.resolve(self.fdoc.root).hash
	self.select(self.there.selected)
	self.push("tsum",address=addr.proto(), value=sum)

def tsum(self, obj, objstring, type):
	if not self.check_selected():return
	if not self.require("address", obj):return
	if not self.require("value", obj):return
	# Compare to our own hash
	addr = address.Address(obj['address'])
	sum = addr.resolve(self.fdoc.root).hash
	if sum != obj['value']:
		self.sendop(self.there.selected, addr)
		self.push("get", address=addr.proto(), depth=1)

def subscribe(self, obj, objstring, type):
	if "docnames" not in obj:
		if not self.check_selected(): return
		obj[docnames] = [self.there.selected]
	for name in obj['docnames']:
		self.docs[name].subscribed = True
		self.pool_push({"type":"subscribe", "docname":name})
		self.there.subscriptions.add(name)

def unsubscribe(self, obj, objstring, type):
	if "docnames" in obj:
		if len(obj['docnames']) > 0:
			for name in obj['docnames']:
				self.there.subscriptions.discard(name)
		else:
			self.there.subscriptions.clear()
	else:
		if not self.check_selected(): return
		self.there.subscriptions.discard(self.there.selected)

def error(self, obj, objstring, type):
	print obj

Core = ("core", {
	"select"     : select,
	"op"         : op,
	"get"        : get,
	"check"      : check,
	"tsum"       : tsum,
	"subscribe"  : subscribe,
	"unsubscribe": unsubscribe,
	"error"      : error
})
