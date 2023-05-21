from uno.enums import *
from uno.card import Card
from uno.deck import Deck
from uno.table import Table
from uno.player import Player
from uno.utils import *
from System.weighted_picker import WeightedPicker

import random

class Game:
    def __init__(self, players, stage_bit, sound, table=None, deck=None):
        self.sound = sound
        self.players = players
        if table:
            self.table = table
        else:
            self.table = Table()

        if deck:
            self.deck = deck
        else:
            self.deck = Deck({"number": 1, "special": 1, "wild": 2})
        self.players_turn = CycleIterator(players)
        self.stage_bit = stage_bit
        self.ai_players = []
        for player in players:
            if player.is_ai:
                self.ai_players.append(player)

        self.uno_player = None

        if not table and not deck:
            self.draw_setting()
            self.table.put(self.deck.draw())
            if self.stage_bit & (1 << 2) and (not self.table.top().is_special()):
                self.deck.pop_all()

    def remove_player(self, player):
        self.players.remove(player)
        self.players_turn.update()

    def draw_setting(self, default_card_num = 5):
        if self.stage_bit & (1 << 2):
                n = (len(self.deck.stack) // len(self.players)) - 1
                for player in self.players:
                    self.draw_by_type(player, n)
        else:
            for player in self.players:
                self.draw_by_type(player, default_card_num)
        
    def draw_by_type(self, player, n = 1):
        if player.is_ai:
            match player.index:
                case 1:
                    self.weighted_draw(player, {"number": 2, "special": 3}, n)
                case _:
                    self.draw(player, n)
        else:
            self.draw(player, n)
        

    def draw(self, player, n=1):
        self.sound.card_submission.play()
        n = min(n, len(self.deck.stack))
        player.hand.extend([self.deck.draw() for _ in range(n)])
        player.uno = None
        
    def weighted_draw(self, player, weights, n=1):
        picker = WeightedPicker(weights)
        n = min(n, len(self.deck.stack))
        player.hand.extend([picker.pick_card(self.deck.stack) for _ in range(n)])

    def deal(self, player, players_number, card):
        if self.table.playable(card):
            self.sound.card_selection.play()
            
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
                    card.color = None
                    
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
        self.sound.card_submission.play()
        player1.hand, player2.hand = player2.hand, player1.hand
        self.handle_uno_state(player1)
        self.handle_uno_state(player2)
        
    def get_random_AIplayer(self):
        return random.choice(self.ai_players)
        
    def handle_uno_state(self, player):
        if len(player.hand) <= 2:
            player.uno = player
        else:
            player.uno = None

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