from uno.enums import *
from uno.card import Card
from uno.deck import Deck
from uno.table import Table
from uno.player import Player
from uno.utils import *
from System.weighted_picker import WeightedPicker

class Game:
    def __init__(self, players, callback, stage_index):
        self.players = players
        self.table = Table()
        self.deck = Deck({"number": 1, "special": 1, "wild": 0})
        self.players_turn = CycleIterator(players)
        self.callback = callback
        self.stage_index = stage_index

        self.table.put(self.deck.draw()) # TODO: 첫 카드가 숫자 카드가 아닐 때
        self.draw_setting()
        

    def draw_setting(self, default_card_num = 7):
        if(self.stage_index == 0):
            for player in self.players:
                self.draw(player, default_card_num)
        elif(self.stage_index == 1):
            self.draw(self.players[0], default_card_num)
            self.weighted_draw(self.players[1],{"number": 2, "special": 3}, default_card_num)
            # 가중치 하드코딩? 어딘가에 저장해 놓는 것이 좋을지
        elif(self.stage_index == 2):
            n = len(self.deck.stack) // len(self.players)
            for player in self.players:
                self.draw(player, n)
        elif(self.stage_index == 3):
            for player in self.players:
                self.draw(player, default_card_num)
        

    def draw(self, player, n=1):
        n = min(n, len(self.deck.stack))
        player.hand.extend([self.deck.draw() for _ in range(n)])
        
    def weighted_draw(self, player, weights, n=1):
        picker = WeightedPicker(weights)
        n = min(n, len(self.deck.stack))
        player.hand.extend([picker.pick_card(self.deck.stack) for _ in range(n)])

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
        
        if player.is_ai:
            card = player.choose_card(self.table)
            
        if card:
            if self.deal(player, card):
                next(self.players_turn)
        else:
            self.draw(player)
            next(self.players_turn)

        return True

    def turn(self):
        return self.players_turn.current()