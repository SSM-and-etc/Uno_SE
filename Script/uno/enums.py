from enum import auto, StrEnum

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
    CARD_DRAW = auto()

    @classmethod
    def NUMBER(cls):
        return [cls.CARD_0, cls.CARD_1, cls.CARD_2, cls.CARD_3, cls.CARD_4, cls.CARD_5, cls.CARD_6, cls.CARD_7, cls.CARD_8, cls.CARD_9]

    @classmethod
    def SPECIAL(cls):
        return [cls.CARD_SKIP, cls.CARD_REVERSE, cls.CARD_PLUS2, cls.CARD_CHANGECOLOR, cls.CARD_DRAW]

    @classmethod
    def WILD(cls):
        return [cls.CARD_CHANGECOLOR, cls.CARD_DRAW]

    def is_number(self):
        return self in self.NUMBER()

    def is_special(self):
        return self in self.SPECIAL()
    
    def is_wild(self):
        return self in self.WILD()
            