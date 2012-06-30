class EventGrid(object):
    # Stores callbacks (they should take args (evgrid, label))
    def __init__(self, labels=[]):
        self.handlers = {}
        self.setup_labels(labels+['all'])

    def setup_labels(self, labels):
        for i in labels:
            self[i]

    def register(self, label, func):
        # Move to end if already registered
        if func in self[label]:
            self[label].remove(func)
        self[label].append(func)

    def happen(self, label, data={}):
        callbacks = list(self[label])
        if label != "all":
            callbacks += self['all']
        for i in callbacks:
            i(self, label, data)

    def __getitem__(self, label):
        if not label in self:
            self[label] = []
        return self.handlers[label]

    def __setitem__(self, label, value):
        self.handlers[label] = value

    def __delitem__(self, label):
        del self.handlers[label]

    def __contains__(self, label):
        return label in self.handlers
