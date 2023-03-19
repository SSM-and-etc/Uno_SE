from uno.enums import *
from uno.card import Card
from uno.deck import Deck
from uno.player import Player
from itertools import cycle

class Game:
    def __init__(self, players, n=7):
        self.table = []
        self.players = players
        self.deck = Deck()
        self.turn = cycle

        self.init_deal(n)
        self.table.append(self.deck.draw()) # TODO: 첫 카드가 숫자 카드가 아닐 때

    def init_deal(self, n):
        for player in self.players:
            player.hand.extend([self.deck.draw() for _ in range(n)])

    def play():
        pass