class Player:
    def __init__(self, tag=None):
        self.hand = []
        self.tag = tag

    def __repr__(self):
        return f"<Player {self.tag}: {self.hand}>"
    