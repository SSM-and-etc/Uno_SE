from uno.card import Card
from uno.enums import *
import random

class Deck:
    def __init__(self, n={"number": 2, "special": 2, "wild": 1}):
        self.stack = []

        for card_type in CardType.NUMBER():
            for card_color in CardColor:
                self.stack.extend([Card(card_type, card_color) for _ in range(n["number"])])

        for card_type in CardType.SPECIAL():
            if card_type.is_wild():
                self.stack.extend([Card(card_type, None) for _ in range(n["wild"])])
            
            else:
                for card_color in CardColor:
                    self.stack.extend([Card(card_type, card_color) for _ in range(n["special"])])
        
        self.shuffle()
        
    def shuffle(self):
        random.shuffle(self.stack)

    def draw(self):
        return self.stack.pop()
    