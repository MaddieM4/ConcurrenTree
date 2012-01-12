import json
import traceback

from ConcurrenTree.util.hasher import strict

from errors import errors
from ext import core, extension

nullbyte = "\x00"

class BCPConnection(object):
	''' A connection between two Peers '''

	def __init__(self, stream, extensions = []):
		''' 
			stream - (input, output) tuple of Queues.
			extensions - a list of extension objects.
		'''
		self.poolsubs = {}
		self.buffer = ""
		self.last_buffer = ""

		self.stream = stream
		self.closed = False

		self._queued_extensions = [core.Core()] + extensions
		self.extensions = {}

	def run(self):
		self.load_extensions(self._queued_extensions)
		try:
			while 1:
				self.read()
				self.frame()
		except IOError:
			print "Connection closed"


	def load_extensions(self, extensions=[]):
		for ext in extensions:
			if ext.name not in self.extensions:
				self.extensions[ext.name] = ext
		self.push("extensions", available=self.extensions.keys())

	def clear_extensions(self):
		self.extensions = {}
		self.load_extensions([core.Core()])

	# STREAM INPUT

	def read(self):
		''' Reads raw data into the buffer '''
		if self.closed:
			raise IOError("Connection Closed")
		value = self.input.get()
		if value == "":
			self.close()
			raise IOError("Connection Closed")
		self.buffer += value

	def inject(self, string):
		self.input.put(string)

	def frame(self):
		''' Parses buffer into frames, as many as are in the buffer '''
		if self.last_buffer != self.buffer:
			self.last_buffer = self.buffer
			print "Buffer:", repr(self.buffer)
		if nullbyte in self.buffer:
			length = self.buffer.index(nullbyte)
			try:
				self.recv_frame(self.buffer[:length])
			finally:
				self.buffer = self.buffer[length+1:]
				self.frame()

	def recv_frame(self, msg):
		''' Processes a raw frame before passing it to self.analyze '''

		print "recving message:",msg
		try:
			obj = json.loads(msg)
		except ValueError:
			self.error(451) # Bad JSON
			return
		if type(obj)!=dict:
			self.error(454) # Wrong root type
			return
		try:
			self.analyze(obj)
		except:
			traceback.print_exc()
			self.error(500)

	# STREAM OUTPUT

	def push(self, msgtype, **kwargs):
		''' Convenience function for sending a message with a type'''
		kwargs['type'] = msgtype
		self.send(kwargs)

	def send(self, msg):
		''' Send a message dict to remote peer '''
		self.send_frame(strict(msg)+nullbyte)

	def send_frame(self, frame):
		''' Send a textual frame to the remote end or raise IOError '''
		if self.closed:
			raise IOError("Connection Closed")
		print "sending message:", frame
		self._send(frame)

	def _send(self, frame):
		''' Underlying function to put a string in the output queue '''
		self.output.put(frame)

	# MESSAGE ANALYSIS

	def analyze(self, obj):
		''' 
			Apply a message as a piece of remote communication.
		'''
		for ext in self.extensions:
			#print "Trying extension "+repr(self.extensions[ext].name)
			try:
				return self.extensions[ext].process(self, obj)
			except extension.TryAnother:
				pass
		self.error(401, data = obj['type']) # Unknown Message Type

	# MISC

	def error(self, num=500, details="", data=None):
		if num in errors and not details:
			details = errors[num]
		if data != None:
			self.push("error", code=num, details=details, data=data)
		else:
			self.push("error", code=num, details=details)

	@property
	def input(self):
		return self.stream[0]

	@property
	def output(self):
		return self.stream[1]

	def close(self):
		self.closed = True

def QueuePair():
	from Queue import Queue
	A = Queue()
	B = Queue()
	return [(A, B), (B, A)]
