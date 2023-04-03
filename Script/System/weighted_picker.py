from bisect import bisect_left, bisect_right
import random

class WeightedPicker():
    def __init__(self, weights={"number": 1, "special": 1}): #가중치는 정수로 전달
        self.weight = weights
        
    def draw(self, deck, player, n=1): # game.py로 옮길까?
        n = min(n, len(deck))
        player.hand.extend([self.pick_card(deck) for _ in range(n)])
        
    def pick_card(self, deck):
        if len(deck) == 0:
            return None
        
        weight_table, table_end = self.get_weight_table(deck)
            
        rand_number = random.randrange(table_end)
        picked_index = bisect_left(weight_table, rand_number)
        picked_card = deck[picked_index]
        del deck[picked_index]
        
        return picked_card
    
    def get_weight_table(self, deck):
        acc_weight = 0
        acc_weights = []
        for card in deck:
            if card.is_number():
                acc_weight += self.weight["number"]
            elif card.is_special(): # 카드 종류 더 추가되는 것 없으면 성능 개선할 때 else로 변경?
                acc_weight += self.weight["special"]
                
            acc_weights.append(acc_weight)
            
        return acc_weights, acc_weight
        