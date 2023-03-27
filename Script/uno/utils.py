class CycleIterator:
    def __init__(self, data):
        self.data = data
        self.n = len(data)
        self.i = 0
        self.forward = True

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.forward:
            return self.next()
        else:
            return self.prev()

    def look_next(self):
        if self.forward:
            return self.data[(self.i + 1) % self.n]
        else:
            return self.data[(self.i - 1) % self.n]

    def reverse(self):
        self.forward = not self.forward

    def next(self, step=1):
        self.i = (self.i + step) % self.n
        return self.data[self.i]

    def prev(self, step=1):
        self.i = (self.i - step) % self.n
        return self.data[self.i]

    def current(self):
        return self.data[self.i] 