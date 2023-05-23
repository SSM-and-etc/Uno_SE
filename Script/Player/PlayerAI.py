from uno.player import Player
from uno.enums import *

import random

class PlayerAI(Player): 
    def __init__(self, index = 0, tag=None):
        self.index = index # 0: default, n: stage n (n > 0)
        super().__init__(tag, True, index)
        
        
    def choose_card(self, table):
        if self.index == 1:
            return self.choose_card_stage1(table)
        else:
            return self.choose_card_default(table)
        
    def choose_color(self, table_color):
        possible_colors = []
        for card_color in CardColor:
            if table_color != card_color:
                possible_colors.append(card_color)
                
        return random.choice(possible_colors)
    
    def choose_card_default(self, table):
        picked_card = None
        possible_hand = []
        
        for card in self.hand:
            if table.playable(card):
                possible_hand.append(card)
                
        if len(possible_hand) != 0:
            picked_card = random.choice(possible_hand)
    
        return picked_card
    
    def choose_card_stage1(self, table):
        picked_card = None
        possible_hand = []
        
        for card in self.hand:
            if table.playable(card):
                if(card.card_type == CardType.CARD_REVERSE or
                   card.card_type == CardType.CARD_SKIP):
                    return card
                possible_hand.append(card)
                
        if len(possible_hand) != 0:
            picked_card = random.choice(possible_hand)
    
        return picked_card
    
    