from uno.card import *
import random

class Table:
    def __init__(self):
        self.cards = []
        self.color = None

    def __repr__(self):
        return f"{self.cards} / {self.color}"
    
    def get_color(self):
        if self.color:
            return self.color
        else:
            return self.cards[-1].color
        
    def change_color(self, color):
        if self.top().card_type.is_color():
            
            new_card = Card(self.top().card_type, color)
            self.put(new_card)
        else:    
            self.color = color
        
    def change_random_color(self):
        self.color = random.choice(list(CardColor))
    
    def put(self, card):
        self.cards.append(card)
        self.color = None

    def top(self):
        return self.cards[-1]

    def playable(self, card):
        if card:
            if card.card_type.is_wild():
                return True
            else:
                return card.card_type == self.top().card_type or self.get_color() == card.color
        else:
            return False