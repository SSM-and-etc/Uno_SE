from uno.enums import *
from uno.card import Card
from uno.deck import Deck
from uno.table import Table
from uno.player import Player
from uno.utils import *
from System.weighted_picker import WeightedPicker

import random

class Game:
    def __init__(self, players, stage_index):
        self.players = players
        self.table = Table()
        self.deck = Deck({"number": 1, "special": 1, "wild": 10})
        self.players_turn = CycleIterator(players)
        self.stage_index = stage_index

        self.table.put(self.deck.draw()) # TODO: 첫 카드가 숫자 카드가 아닐 때
        self.draw_setting()
        

    def draw_setting(self, default_card_num = 7):
        match self.stage_index:
            case 1:
                self.draw(self.players[0], default_card_num)
                self.weighted_draw(self.players[1],{"number": 2, "special": 3}, default_card_num)
                # 가중치 하드코딩? 어딘가에 저장해 놓는 것이 좋을지
            case 2:
                n = len(self.deck.stack) // len(self.players)
                for player in self.players:
                    self.draw(player, n)
            case _: # 0, 3, 4
                for player in self.players:
                    self.draw(player, default_card_num)
        

    def draw(self, player, n=1):
        n = min(n, len(self.deck.stack))
        player.hand.extend([self.deck.draw() for _ in range(n)])
        
    def weighted_draw(self, player, weights, n=1):
        picker = WeightedPicker(weights)
        n = min(n, len(self.deck.stack))
        player.hand.extend([picker.pick_card(self.deck.stack) for _ in range(n)])

    def deal(self, player, players_number, card):
        if self.table.playable(card):
            if card.is_number():
               self.table.put(card) 

            else:
                if card.card_type == CardType.CARD_PLUS2:
                    self.draw(self.players_turn.look_next(), 2)

                elif card.card_type == CardType.CARD_REVERSE:
                    if players_number == 2:
                        next(self.players_turn)
                    else:    
                        self.players_turn.reverse()

                elif card.card_type == CardType.CARD_SKIP:
                    next(self.players_turn)
                    
                elif card.card_type == CardType.CARD_RNUMBER:
                    rnumber_card = Card(random.choice(CardType.NUMBER()), card.color)
                    self.table.put(rnumber_card)

                elif card.card_type == CardType.CARD_CHANGECOLOR:
                    print(card.color)
                    self.table.change_color(card.color)
                    
                elif card.card_type == CardType.CARD_DRAW:
                    self.draw(self.players_turn.look_next(), 4)
                    
                elif card.card_type == CardType.CARD_SWAP:
                    player.hand.remove(card)
                    
                    players_list = self.players.copy()
                    players_list.remove(player)
                    rand_player = random.choice(players_list)
                    self.hand_swap(player, rand_player)
                    return True
                    

            player.hand.remove(card)
            return True

        else:
            return False

    def hand_swap(self, player1, player2):
        player1.hand, player2.hand = player2.hand, player1.hand

    def play(self, player, players_number, card=None):
        current_player = self.turn()
        if current_player != player:
            return False
        
        if card:
            if self.deal(player, players_number, card):
                next(self.players_turn)

        else:
            self.draw(player)
            next(self.players_turn)

        return True

    def turn(self):
        return self.players_turn.current()