import user

class Auth(object):
    ''' Key-value store for storage spaces keyed on username. '''

    def __init__(self):
        self.contents = {}

    def make(self, username, password):
        if username in self:
            return self[username]
        else:
            self[username] = user.UserStorage(username, password)
            return self[username] 

    def __getitem__(self, username):
        return self.contents[username]

    def __setitem__(self, username, storage):
        self.contents[username] = storage

    def __delitem__(self, username):
        del self.contents[username]

    def __contains__(self, username):
        return username in self.contents
