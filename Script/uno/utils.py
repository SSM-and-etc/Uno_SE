class CycleIterator:
    def __init__(self, data):
        self.data = data
        self.n = len(data)
        self.i = -1
        self.forward = True
        self.init_flag = True # 처음에 prev하면 두 칸 뒤로가버림

    def __iter__(self):
        return self
    
    def __next__(self):
        if self.forward:
            return self.next()
        else:
            return self.prev()

    def reverse(self):
        self.forward = not self.forward

    def next(self, step=1):
        self.init_flag = False
        self.i = (self.i + step) % self.n
        return self.data[self.i]

    def prev(self, step=1):
        if self.init_flag:
            self.i += 1
            self.init_flag = False
        self.i = (self.i - step) % self.n
        return self.data[self.i]