import os, os.path
import json

from ConcurrenTree.model.document import Document
from ConcurrenTree.util.storage import BaseStorage
from ConcurrenTree.util import hasher

STORAGE_DIR = os.path.join('~', '.ConcurrenTree', 'storage')

class FileStorage(BaseStorage):
    """Storage interface, including caching"""
    def __init__(self, find=None, dir=STORAGE_DIR, encryptor=None):
        BaseStorage.__init__(self, find=find, encryptor=encryptor)
        self._dir = os.path.expanduser(dir)
        self._cache = {}
        self._dirty = set()
        
    def get(self, x):
        if x in self._cache:
            return self._cache[x]
        else:
            return self.load(x)

    def set(self, doc, docname):
        self._cache[docname] = doc
        self._dirty.add(docname) 

    def delete(self, docname):
        del self._cache[docname]
        self._dirty.remove(docname)
        path = self.filename(docname)
        if os.path.exists(path):
            os.remove(path)

    def has(self, docname):
        return docname in self._cache or os.path.exists(self.filename(docname))

    def op(self, docname, op):
        BaseStorage.op(self, docname, op)
        self._dirty.add(docname)

    def store(self, docname):
        with open(self.filename(docname), 'w') as f:
            f.write(
                self.encrypt(
                      str(self[docname])
                    )
                )

    def load(self, docname):
        path = self.filename(docname)
        if os.path.exists(path):
            with open(path, 'r') as f:
                contents = self.decrypt(f.read())
                json_file = json.loads(contents)
                doc = Document({})
		doc.load(json_file)
            self._cache[x] = doc
            return doc
        else:
            raise NameError(docname)

    def flush(self):
        for docname in self._dirty:
            self.store(docname)
            self._dirty.remove(docname)

    def filename(self, docname):
        return os.path.join(self._dir, 
            hasher.sum(self.encrypt(docname))
        )

    @property
    def subscribed(self):
        ''' Docnames that you are subscribed to. '''
        return [i for i in self._cache if self._cache[i].subscribed]


class FileStorageFactory(object):
    def __init__(self, storageDir=STORAGE_DIR, find=None, encryptorFactory=None):
        self.dir = storageDir
        self.find = find
        self.encryptorFactory = encryptorFactory

    def make(self, username, password):
        return FileStorage(self.find,
            self.filename(username),
            self.encryptor(username, password)
        )

    def new(self, username, password, key=None):
        self.encryptorFactory.new(username, password, key)
        os.makedirs(self.filename(username))
        return self.make(username, password)

    def verify(self, username, password):
        try:
            self.encryptor(username, password)
            return True
        except:
            raise ValueError("Bad username or password.")

    def encryptor(self, username, password):
        if self.encryptorFactory:
            return self.encryptorFactory.make(username, password)

    def filename(self, username):
        return os.path.join(self.dir, hasher.sum(username))
