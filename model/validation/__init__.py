__all__ = [
	'cmdline',
	'hello',
	'invitation',
	'operation',
	'queue',
	'request',
]

from invitation import InvitationRequest
from operation  import OperationRequest
from hello      import HelloRequest

from queue import ValidationQueue

def make(request_type, *args, **kwargs):
	if   request_type == "invitation":
		return InvitationRequest(*args, **kwargs)
	elif request_type == "operation":
		return OperationRequest(*args, **kwargs)
	elif request_type == "hello":
		return HelloRequest(*args, **kwargs)
	else:
		raise ValueError("Unknown request type %r" % request_type)

