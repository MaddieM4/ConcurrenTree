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

    def backend_data(self):
        '''
        The data tuple for the dbcps backend.

        >>> UserStorage('abc', 'def').storage.get_dbh().handle
        'abc'
        '''
        return ('ramdict', ['rotate', 51], self.username)

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
        doc = self.doc_get(docname)
        if not doc.is_applied(op):
            doc.apply(op)
            self.event("op", docname, op)

    # Document cache manipulation

    def doc_get(self, docname):
        # Retrieve a document from cache, creating from CPS if necessary.
        if docname in self.cache:
            return self.cache[docname]
        doc = Document({})
        if docname in self:
            json_data = json.loads(self[docname])
            doc.load(json_data)
        self.doc_set(docname, doc)
        return doc

    def doc_set(self, docname, value):
        # Set a doc in the cache
        self.cache[docname] = value

    def doc_del(self, docname):
        # Remove a document from the cache.
        del self.cache[docname]

    def doc_reload(self, docname):
        # Convenience function for del & get
        self.doc_del(docname)
        self.doc_get(docname)

    def doc_save(self, docname):
        # Save the current document state to CPS
        doc = self.doc_get(docname)
        self[docname] = doc.serialize()

    # Dict access to strings

    def __getitem__(self, k):
        '''
        >>> s = UserStorage('abc', 'def') 
        >>> s['x']
        Traceback (most recent call last):
        KeyError: 'x'
        >>> s['x'] = 'y'
        >>> s['x']
        'y'
        '''
        return self.storage[k]

    def __setitem__(self, k, i):
        self.storage[k] = i

    def __delitem__(self, k):
        del self.storage[k]

    def __contains__(self, k):
        '''
        >>> s = UserStorage('abc', 'def') 
        >>> 'x' in s
        False
        >>> s['x'] = "Shaboygan"
        >>> 'x' in s
        True
        >>> del s['x']
        >>> 'x' in s
        False
        '''
        return k in self.storage
