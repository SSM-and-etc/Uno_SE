class Player:
    def __init__(self, tag=None, is_ai = False, index = -1):
        self.hand = []
        self.tag = tag
        self.is_ai = is_ai
        self.uno = None
        self.index = index

    def __repr__(self):
        return f"<Player {self.tag}: {self.hand}>"

    def __eq__(self, value):
        return self.tag == value.tag