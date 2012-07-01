class EventGrid(object):
    # Stores callbacks (they should take args (evgrid, label))
    def __init__(self, labels=[]):
        self.handlers = {}
        self.reset_current()
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
        try:
            self.current_label = label
            callbacks = list(self[label])
            if label != "all":
                callbacks += self['all']
            for i in callbacks:
                self.current_func = i
                i(self, label, data)
        finally:
            self.reset_current()

    def detach(self, label=None, func=None):
        # Can be called with no arguments during a callback to detach itself,
        # or with arguments outside a handler to detach a specific callback.
        label = label or self.current_label
        func  = func  or self.current_func
        if label and func:
            self[label].remove(func)
        else:
            raise ValueError("Insufficient detach information: (%r, %r)" % (self.current_label, self.current_func))

    def reset_current(self):
        self.current_label = None
        self.current_func  = None

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
