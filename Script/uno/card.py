from uno.enums import *

class Card:
    def __init__(self, card_type, color=None):
        self.card_type = card_type
        self.color = color

    def __repr__(self):
        return f"({self.card_type} / {self.color})"

    def playable(self, card):
        if CardType.is_wild(self.card_type):
            return True
        else:
            return self.card_type == card.card_type or self.color == card.color