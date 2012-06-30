import json
from document import Document
from dbcps.storage import Storage

class UserStorage(object):
    '''
    Wraps dbcps storage and centralizes event callbacks.
    '''
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.cache = {}
        self.event_listeners = set()
        self.storage = Storage([self.backend_data()])
        self.__getitem__ = self.storage.__getitem__
        self.__setitem__ = self.storage.__setitem__
        self.__delitem__ = self.storage.__delitem__
        self.__contains__ = self.storage.__contains__

    def backend_data(self):
        '''
        The data tuple for the dbcps backend.

        >>> us = UserStorage('abc', 'def')
        >>> s = us.storage
        >>> s.get_dbh().handle
        'abc'
        >>> s['x']
        Traceback (most recent call last):
        KeyError: 'x'
        >>> s['x'] = 'y'
        >>> s['x']
        'y'
        '''
        return ('ramdict', ['aes', self.password], self.username)

	# Events

    def listen(self, handler):
        # handler(typestr, docname, data)
        self.event_listeners.add(handler)

    def unlisten(self, handler):
        self.event_listeners.remove(handler)

    def event(self, typestr, docname, data):
        for ear in self.event_listeners:
            ear(typestr, docname, data)

    def op(self, docname, op):
        doc = self.doc(docname)
        if not doc.is_applied(op):
            doc.apply(op)
            self.event("op", docname, op)

    def doc(self, docname):
        if docname in self.cache:
            return self.cache[docname]
        json_data = json.loads(self[docname])
        doc = Document({})
        doc.load(json_data)
        self.cache[docname] = doc
        return doc
