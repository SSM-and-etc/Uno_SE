from bisect import bisect_left, bisect_right
import random

class WeightedPicker():
    def __init__(self, weights={"number": 1, "special": 1}): #가중치는 정수로 전달
        self.weight = weights
        
        
    def pick_card(self, deck):
        if len(deck) == 0:
            return None
        
        acc_weight = 0
        acc_weights = []
        for card in deck:
            if card.is_number():
                acc_weight += self.weight["number"]
            elif card.is_special(): # 카드 종류 더 추가되는 것 없으면 성능 개선할 때 else로 변경?
                acc_weight += self.weight["special"]
                
            acc_weights.append(acc_weight)
            
        rand_number = random.randrange(acc_weight)
        picked_index = bisect_left(acc_weights, rand_number)
        picked_card = deck[picked_index]
        del deck[picked_index]
        
        return picked_card
        