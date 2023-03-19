from enum import Enum, auto

class StrEnum(str, Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name
    
    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name 

class CardColor(StrEnum):
    RED = auto()
    GREEN = auto()
    BLUE = auto()
    YELLOW = auto()

class CardType(StrEnum):
    CARD_0 = auto()
    CARD_1 = auto()
    CARD_2 = auto()
    CARD_3 = auto()
    CARD_4 = auto()
    CARD_5 = auto()
    CARD_6 = auto()
    CARD_7 = auto()
    CARD_8 = auto()
    CARD_9 = auto()
    CARD_SKIP = auto()
    CARD_REVERSE = auto()
    CARD_PLUS2 = auto()
    CARD_CHANGECOLOR = auto()

    NUMBER = [CARD_0, CARD_1, CARD_2, CARD_3, CARD_4, CARD_5, CARD_6, CARD_7, CARD_8, CARD_9]
    SPECIAL = [CARD_SKIP, CARD_REVERSE, CARD_PLUS2, CARD_CHANGECOLOR]
    WILD = [CARD_CHANGECOLOR]

    def is_special(cardType):
        return cardType in CardType.SPECIAL
    
    def is_wild(cardType):
        return cardType in CardType.WILD
            