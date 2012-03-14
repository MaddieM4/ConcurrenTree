import traceback
import sys

class Guard(object):
	def __enter__(self):
		pass

	def __exit__(self, exc_type, exc_value, exc_traceback):
		if not exc_traceback:
			return True
		print "Traceback",exc_traceback,"caught by", self
		traceback.print_exception(exc_type, exc_value, exc_traceback)
		return True
