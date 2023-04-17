from uno.enums import *

class Card:
    def __init__(self, card_type, color=None):
        self.card_type = card_type
        self.color = color

    def __repr__(self):
        return f"({self.card_type} / {self.color})"
        
    def is_number(self):
        return self.card_type.is_number()

    def is_special(self):
        return self.card_type.is_special()
    
    def is_wild(self):
        return self.card_type.is_wild()

    def is_color(self):
        return self.card_type.is_color()
