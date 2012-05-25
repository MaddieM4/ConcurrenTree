# Core handlers

from extension import *
from ConcurrenTree.model import operation, address

class Core(Extension):
	def __init__(self):
		Extension.__init__(self, "core", {
			"error": error,
			"extensions": extensions
		})

def error(self, conn, obj):
	print obj

def extensions(self, conn, obj):
	conn.error(401)
