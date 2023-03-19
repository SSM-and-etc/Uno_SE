from uno.enums import *
from uno.card import Card
from uno.deck import Deck
from uno.player import Player
from uno.utils import *

class Game:
    def __init__(self, players, n=7):
        self.table = []
        self.players = players
        self.deck = Deck()
        self.players_turn = CycleIterator(players)

        for player in self.players:
            self.draw(player, n)
        self.table.append(self.deck.draw()) # TODO: 첫 카드가 숫자 카드가 아닐 때

    def draw(self, player, n=1):
        player.hand.extend([self.deck.draw() for _ in range(n)])

    def deal(self, player, card):
        if self.table[-1].playable(card):
            if card.is_number():
               self.table.append(card) 

            elif card.is_special():
                if card == CardType.CARD_PLUS2:
                    self.draw(self.players_turn.look_next(), 2)

                elif card == CardType.CARD_REVERSE:
                    self.players_turn.reverse()

                elif card == CardType.CARD_SKIP:
                    next(self.players_turn)

            #elif card.is_wild():
            #    if card == CardType.CARD_CHANGECOLOR:

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

        return True

    def turn(self):
        return self.players_turn.current()