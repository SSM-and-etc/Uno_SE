import pytest
from System.weighted_picker import WeightedPicker
from uno.deck import Deck
import copy

def pick_card():
    deck = Deck({"number": 3, "special": 10, "wild": 0}).stack
    picker = WeightedPicker({"number":2,"special":3})
    
    return picker.pick_card(deck)
    
def get_err():
    number = 0
    special = 0
    for _ in range(1000):
        if pick_card().card_type.is_number():
            number += 1
        else :
            special += 1

    print("숫자 카드: " + str(number))
    print("기술 카드: " + str(special))
    # print("오차: " + str((400 - number)/4) + " %")
    
    return abs((400 - number)/4)
    
def test_answer():
    assert get_err() <= 5   
    
test_answer()