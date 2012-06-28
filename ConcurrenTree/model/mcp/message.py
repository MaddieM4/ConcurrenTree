from ejtp.util.crashnicely import Guard
from ejtp.util.hasher import strict
from ConcurrenTree.model import operation
from sys import stderr
import random
import json

class MessageProcessor(object):

	# Convenience accessors

	@property
	def client(self):
		return self.gear.client

	@property
	def hosts(self):
		return self.gear.hosts

	@property
	def interface(self):
		return self.gear.interface

class Writer(MessageProcessor):
	def __init__(self, gear):
		self.gear = gear

	def send(self, target, data, wrap_sender=True):
		data['ackc'] = str(random.randint(0, 2**32))
		self.client.write_json(target, data, wrap_sender)

	# Message creators

	def hello(self, target):
		# Send your EJTP encryption credentials to an interface
		self.send(target,
			{
				'type':'mcp-hello',
				'interface':self.interface,
				'key':self.hosts.crypto_get(self.interface),
			},
			False,
		)

	def error(self, target, code=500, message="", data={}):
		self.send(target, {
			"type":"mcp-error",
			"code":code,
			"msg":message,
			"data":data
		})

	def op(self, docname, op, targets=[]):
		# Send an operation frame.
		# targets defaults to document.routes_to for every sender.
		proto = op.proto()
		proto['type'] = 'mcp-op'
		proto['docname'] = docname

		targets = targets or self.gear.document(docname).routes_to(self.interface)

		for i in targets:
			self.send(i, proto)

	def pull_index(self, target, docname):
		self.send(target, {
			"type":"mcp-pull-index",
			"docname":docname,
		})

	def index(self, target, docname, hashes):
		self.send(target, {
			"type":"mcp-index",
			"docname":docname,
			"hashes":hashes,
		})

	def pull_snapshot(self, target, docname):
		self.send(target, {
			"type":"mcp-pull-snapshot",
			"docname":docname,
		})

	def snapshot(self, target, docname, snapshot):
		self.send(target, {
			"type":"mcp-snapshot",
			"docname":docname,
			"content":snapshot
		})

	def ack(self, target, codes):
		self.send(target, {
			"type":"mcp-ack",
			"ackr":codes,
		})

class Reader(MessageProcessor):
	def __init__(self, gear):
		self.gear = gear

	def acknowledge(self, content, sender):
		if 'ackc' in content and content['type'] != 'mcp-ack':
			ackc = content['ackc']
			self.gear.writer.ack(sender, [ackc])
			return False
		elif 'ackr' in content and content['type'] == 'mcp-ack':
			return True
		else:
			print>>stderr, "Malformed frame:\n%s" % json.dumps(content, indent=2)

	def read(self, content, sender=None):
		try:
			content = json.loads(content)
		except:
			print "COULD NOT PARSE JSON:"
			print content
		t = content['type']
		if self.acknowledge(content, sender): return
		fname = t.replace('-','_')
		if hasattr(self, fname):
			return getattr(self, fname)(content, sender)
		else:
			print "Unknown msg type %r" % t

	# Message handlers

	def mcp_hello(self, content, sender):
		self.gear.gv.hello(content['interface'], content['key'])

	def mcp_op(self, content, sender):
		docname = content['docname']
		op = operation.Operation(content['instructions'])
		self.gear.gv.op(sender, docname, op)

	def mcp_pull_index(self, content, sender):
		docname = content['docname']
		doc = self.gear.document(docname)
		result = {}
		for x in doc.applied:
			result[x] = self.client.sign(x)
		self.gear.writer.index(sender, docname, result)

	def mcp_index(self, content, sender):
		docname = content['docname']
		hashes = content['hashes']
		sorted_keys = hashes.keys()
		sorted_keys.sort()
		for key in sorted_keys:
			print "%s: %r" % (key, hashes[key])

	def mcp_pull_snapshot(self, content, sender):
		docname = content['docname']
		doc = self.gear.document(docname)
		self.gear.writer.snapshot(sender, docname, doc.flatten())

	def mcp_snapshot(self, content, sender):
		docname = content['docname']
		print strict(content['content'])

	def mcp_error(self, content, sender):
		print "Error from:", sender, ", code", content["code"]
		print repr(content['msg'])
