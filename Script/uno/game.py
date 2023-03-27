from uno.enums import *
from uno.card import Card
from uno.deck import Deck
from uno.table import Table
from uno.player import Player
from uno.utils import *

class Game:
    def __init__(self, players, callback, n=7):
        self.players = players
        self.table = Table()
        self.deck = Deck({"number": 1, "special": 1, "wild": 20})
        self.players_turn = CycleIterator(players)
        self.callback = callback

        for player in self.players:
            self.draw(player, n)
        self.table.put(self.deck.draw()) # TODO: 첫 카드가 숫자 카드가 아닐 때

    def draw(self, player, n=1):
        player.hand.extend([self.deck.draw() for _ in range(n)])

    def deal(self, player, card):
        if self.table.playable(card):
            if card.is_number():
               self.table.put(card) 

            else:
                if card.card_type == CardType.CARD_PLUS2:
                    self.draw(self.players_turn.look_next(), 2)

                elif card.card_type == CardType.CARD_REVERSE:
                    self.players_turn.reverse()

                elif card.card_type == CardType.CARD_SKIP:
                    next(self.players_turn)

                elif card.card_type == CardType.CARD_CHANGECOLOR:
                    self.table.color = self.callback["select_color"]()

            player.hand.remove(card)
            return True

        else:
            return False

    def play(self, player, card=None):
        current_player = self.turn()
        if current_player != player:
            return False
        
        if card:
            if self.deal(player, card):
                next(self.players_turn)
        else:
            self.draw(player)
            next(self.players_turn)

        return True

    def turn(self):
        return self.players_turn.current()