from uno.card import *

def test_playable():
    card = Card(CardType.CARD_0, CardColor.RED)
    card2 = Card(CardType.CARD_1, CardColor.BLUE)
    card3 = Card(CardType.CARD_1, CardColor.RED)

    card_special = Card(CardType.CARD_PLUS2, CardColor.RED)

    assert card.playable(card2) == False
    assert card.playable(card3) == True

    assert card_special.playable(card) == True
    assert card_special.playable(card2) == False