def consider(queue):
	'''
	Takes an iterable, produces a simple approval loop.
	'''
	for request in queue:
		print request
		response = raw_input("Approve, Reject, Defer, or Quit? [a|r|d|q] ")
		if response == 'a':
			request.approve()
		elif response == 'r':
			request.reject()
		elif response == 'q':
			print "Exiting loop..."
			queue.add(request)
			return
		else:
			print "Deferring the choice until later..."
			queue.add(request)
