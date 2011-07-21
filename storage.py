import os.path
import json

from tree import Tree
from encryption import LocalStorageCipher

STORAGE_DIR = os.path.join('~', '.ConcurrenTree', 'storage')


class Storage(object):
    """Storage interface, including caching"""
    def __init__(self):
        self._cache = {}
        
    def __contains__(self, x):
        try:
            self.get(x)
            return True
        except NameError:
            return False

    def __getitem__(self, name):
        return self.get(name)

    def __setitem__(self, name, tree):
        self._cache[name] = tree
            
    def get(self, x):
        if x in self._cache:
            return self._cache[x]
        elif os.path.exists(os.path.join(STORAGE_DIR, x)):
            with open(os.path.join(STORAGE_DIR, x), 'r') as f:
                tree = Tree(
                    json.loads(
                        LocalStorageCipher.decrypt(
                            f.read()
                            )
                        )
                    )
            self._cache[x] = tree
            return tree
        else:
            self[x] = Tree()
            return self[x]
            #raise NameError('Not Found in local storage: Tree with id ' + x)

    def set(self, tree):
        self._cache[tree.id] = tree
    
    def store(self, tree):
        with open(os.path.join(STORAGE_DIR, tree.id), 'w') as f:
            f.write(
                LocalStorageCipher.encrypt(
                    tree.json
                    )
                )

    def dump(self):
        for key, tree in self._cache.items():
            self.store(tree)
            del self._cache[key]
                
