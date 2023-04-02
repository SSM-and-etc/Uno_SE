from uno.player import Player
from uno.enums import *

import random

class Default_AI(Player): 
    def __init__(self, tag=None):
        super().__init__(tag)
        
        
    def play(self, table):
        card = None
        possible_hand = []
        
        for i, card in enumerate(self.hand):
            if table.playable(card):
                possible_hand.append(i)
                
        if len(possible_hand) != 0:
            card = random.choice(possible_hand)
    
        return card

    def choose_color(self, table_color):
        possible_colors = []
        for card_color in CardColor:
            if table_color != card_color:
                possible_colors.append(card_color)
                
        return random.choice(possible_colors)