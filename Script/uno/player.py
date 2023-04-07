class Player:
    def __init__(self, tag=None, is_ai = False):
        self.hand = []
        self.tag = tag
        self.is_ai = is_ai

    def __repr__(self):
        return f"<Player {self.tag}: {self.hand}>"
    