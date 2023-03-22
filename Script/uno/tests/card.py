from uno.card import *
from uno.table import *

def test_playable():
    card_0r = Card(CardType.CARD_0, CardColor.RED)
    card_0b = Card(CardType.CARD_0, CardColor.BLUE)
    card_1b = Card(CardType.CARD_1, CardColor.BLUE)
    card_1r = Card(CardType.CARD_1, CardColor.RED)
    card_specialr = Card(CardType.CARD_PLUS2, CardColor.RED)
    card_wild = Card(CardType.CARD_CHANGECOLOR)

    table = Table()

    table.put(card_0r)
    assert table.playable(card_0r) == True
    assert table.playable(card_1b) == False
    assert table.playable(card_0b) == True
    assert table.playable(card_1r) == True
    assert table.playable(card_specialr) == True
    assert table.playable(card_wild) == True

    table.put(card_specialr)
    assert table.playable(card_0r) == True
    assert table.playable(card_1b) == False
    assert table.playable(card_wild) == True