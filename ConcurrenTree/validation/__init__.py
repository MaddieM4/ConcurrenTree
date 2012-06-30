__all__ = [
	'cmdline',
	'hello',
	'invitation',
	'load',
	'operation',
	'queue',
	'request',
]

from hello      import HelloRequest
from invitation import InvitationRequest
from load       import LoadRequest
from operation  import OperationRequest

from queue import ValidationQueue

def make(request_type, *args, **kwargs):
	if   request_type == "invitation":
		return InvitationRequest(*args, **kwargs)
	elif request_type == "operation":
		return OperationRequest(*args, **kwargs)
	elif request_type == "hello":
		return HelloRequest(*args, **kwargs)
	elif request_type == "load":
		return LoadRequest(*args, **kwargs)
	else:
		raise ValueError("Unknown request type %r" % request_type)

