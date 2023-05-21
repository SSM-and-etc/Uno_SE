import pygame

from uno.game import Game
from uno.player import Player
from uno.enums import CardColor, CardType
from Player.PlayerAI import PlayerAI
from System.option import Option

from GamePlay.game_play import *

import socket

import random

import pickle

import os

class GamePlayClient(GamePlay):
    def __init__(self, main, stage_index = 0):
        self.set_achi_data()
        self.main = main
        self.stage_index = stage_index
        self.user_data = main.user_data
        Asset.user_data = main.user_data
        self.esc = EscMenu(main, self)
        self.on_esc = False
        self.turn_count_gimmick = 1
        self.user_turn_count_gimmick = 1
        self.color_selection = {
            "selecting": False,
            "idx": None,
            "assets": {CardColor.RED: Asset("Extra/red.png", (200, 400)),
                        CardColor.GREEN: Asset("Extra/green.png", (300, 400)),
                        CardColor.BLUE: Asset("Extra/blue.png", (400, 400)),
                        CardColor.YELLOW: Asset("Extra/yellow.png", (500, 400))
            }
        }

        self.assets = {
            "background": Asset("BG/game.png", (0, 0)),
            "deck": Asset("Card/deck.png", (180, 150), mag=0.3),
            "button_uno": Asset("Button/button_uno.png", (600, 250)),
            "table": Asset("Card/deck.png", (380, 150), mag=0.3),
            "color": Asset("Extra/red.png", (625, 150)),
            "cursor": Asset("Button/button_cursor.png", (-100, -100))
        }
        self.fake_assets = {
            "counter": FakeAsset((830, 450, 0, 0))
        }

        self.on_game_gui = False
        self.winner = None
        self.result_asset = Asset("BG/result.png", (0, 0))

        self.card_assets = []
        self.hand_assets = []
        self.animate_assets = []

        self.font_resize() 

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect(("127.0.0.1", 12345))

        self.server = server
        self.server.setblocking(0)

        self.multiplay = True
        self.game = None

    def socket_handle(self):
        query_players = lambda p: self.players[self.players.index(p)]

        try:
            data = pickle.loads(self.server.recv(4096))
            print("CLIENT:", data)
            if data["action"] == "START":
                self.player = data["payload"]["player"]
                self.players = data["payload"]["players"]
                table = data["payload"]["table"]
                deck = data["payload"]["deck"]

                self.player = query_players(self.player)

                self.game = Game(self.players, 0, self.main.sound, table, deck)

                self.pane_assets = []
                i = 0
                for p in self.players:
                    if p == self.player:
                        self.pane_assets.append(FakeAsset((10, 514, 876, 196)))
                    else:
                        self.pane_assets.append(Asset("BG/player_panel.png", (906, 10 + 150 * i)))
                        i += 1

                self.selection = Selection(self.player, self.color_selection)

                self.update_hand()
                self.update_table()

                self.on_game_gui = True
                random.seed(len(self.players))

            elif data["action"] == "PLAY":
                card = data["payload"]["card"]
                player = data["payload"]["player"]
                player = query_players(player)

                if player != self.player:
                    if card:
                        if card.is_color() and card.card_type != CardType.CARD_CHANGECOLOR:
                            filename = card.color + "_" + card.card_type.split("_")[1]
                        else:
                            filename = "wild_" + card.card_type.split("_")[1]
                        pos_x, pos_y, _, _ = self.pane_assets[self.players.index(player)].rect
                        asset = Asset(f"Card/{filename}.png", (pos_x, pos_y), mag=0.3)
                        self.animate_assets.append((asset, self.assets["table"], 50, 0))
                    else:
                        self.animate_assets.append((self.assets["deck"].clone(), self.pane_assets[self.players.index(player)], 50, 0))

                    self.game.play(player, len(self.players), card)

            elif data["action"] == "UNO":
                uno_player = query_players(data["payload"]["uno_player"])
                player = query_players(data["payload"]["player"])

                if player != self.player:
                    self.game.uno_player = uno_player.uno = player

            elif data["action"] == "DISCONNECTED":
                player = query_players(data["payload"]["player"])
                print(player)
                idx = self.players.index(player)
                self.game.remove_player(player)
                self.pane_assets.pop(idx)

                self.update_hand()
                self.update_table()

        except:
            pass

    def display(self, main):
        self.socket_handle()
        if self.game:
            super().display(main)
    
    def counter_event(self):
        if self.counter > 0:
            self.counter -= 1

        if self.counter == 0:
            if self.game.turn() == self.player:
                if self.game.deck.stack:
                    self.animate_assets.append((self.assets["deck"].clone(), self.card_assets[-1], 50, 0))
                    self.play_player(self.game.turn())
                else:
                    self.play_player(self.game.turn())
                    self.update_table()

            self.counter = 15

    def play_player(self, player, card = None):
        # self.game.play() 이후의 self.game.turn()은 순서를 넘겨 받은 플레이어가 됨에 주의
        self.server.send(pickle.dumps({
            "action": "PLAY",
            "payload": {
                "player": player,
                "card": card
            }
        }))
        self.game.play(player, len(self.players), card)
    
    def play_uno(self, uno_player, player):
        self.server.send(pickle.dumps({
            "action": "UNO",
            "payload": {
                "uno_player": uno_player,
                "player": player 
            }
        }))
        self.game.uno_player = uno_player.uno = player