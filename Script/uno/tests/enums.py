from uno.enums import *

def test_enum():
    assert CardType.CARD_0.is_number() == True
    assert CardType.CARD_0.is_special() == False
    assert CardType.CARD_0.is_wild() == False

    assert CardType.CARD_CHANGECOLOR.is_number() == False
    assert CardType.CARD_CHANGECOLOR.is_special() == True
    assert CardType.CARD_CHANGECOLOR.is_wild() == True