import pygame

from uno.game import Game
from uno.player import Player
from uno.enums import CardColor, CardType
from System.option import Option
import socket
import errno
from GamePlay.game_play import * 

import random

import pickle

import os

class GamePlayServer(GamePlay):
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

        self.on_game_gui = True
        self.winner = None
        self.result_asset = Asset("BG/result.png", (0, 0))

        self.card_assets = []
        self.hand_assets = []
        self.animate_assets = []

        self.font_resize() 

        self.no_pause = True
        self.sockets = []
        self.player = Player("Server")
        self.players = [self.player]

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("0.0.0.0", 12345))
        self.sock.listen()
        #self.sock.setblocking(0)

        client = self.sock.accept()
        self.sockets.append(client[0])
        self.players.append(Player("Client"))

        self.sockets.append(None)
        self.players.append(PlayerAI(tag="AI"))

        '''
        client = self.sock.accept()
        self.sockets.append(client[0])
        self.players.append(Player("Client3"))
        print(self.sockets)
        '''

        while True:
            self.game = Game(self.players, 0, main.sound)
            if not self.game.table.top().is_special():
                break
            for p in self.players:
                p.hand.clear()

        for idx, p in enumerate(self.players[1:]):
            if self.sockets[idx]:
                self.sockets[idx].send(pickle.dumps({
                    "action": "START",
                    "payload": {
                        "player": p,
                        "players": self.players,
                        "table": self.game.table,
                        "deck": self.game.deck,
                    }
                }))

        random.seed(len(self.players))

        self.pane_assets = [FakeAsset((10, 514, 876, 196))]
        for i in range(len(self.players)-1):
            self.pane_assets.append(Asset("BG/player_panel.png", (906, 10 + 150 * i)))

        self.selection = Selection(self.player, self.color_selection)

        self.update_hand()
        self.update_table()    

    def socket_handle(self):
        query_players = lambda p: self.players[self.players.index(p)]

        for sock in filter(None, self.sockets):
            sock.setblocking(0)
            try:
                recv = sock.recv(4096)

                for sock2 in filter(None, self.sockets):
                    sock2.send(recv)

                data = pickle.loads(recv)
                print("SERVER:", data)
                if data["action"] == "PLAY":
                    player = query_players(data["payload"]["player"])
                    card = data["payload"]["card"]

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

                    self.game.uno_player = uno_player.uno = player

            except socket.error as e:
                if e.errno == errno.ECONNRESET:
                    print(e)
                    idx = self.sockets.index(sock) + 1
                    player = self.players[idx]
                    print("DISCONNECTED:", sock)
                    print(player)

                    self.sockets.remove(sock)
                    self.game.remove_player(player)
                    self.pane_assets.pop()

                    self.update_hand()
                    self.update_table()

                    for sock2 in filter(None, self.sockets):
                        sock2.send(pickle.dumps({
                            "action": "DISCONNECTED",
                            "payload": {"player": player},
                        }))
            except:
                pass
        

    def display(self, main):
        self.socket_handle()
        super().display(main)

    def play_player(self, player, card = None):
        for sock in filter(None, self.sockets):
            print(sock, player, card)
            sock.send(pickle.dumps({
                "action": "PLAY",
                "payload": {
                    "player": player,
                    "card": card,
                }
            }))
        self.game.play(player, len(self.players), card)
    
    def play_uno(self, uno_player, player):
        for sock in filter(None, self.sockets):
            sock.send(pickle.dumps({
                "action": "UNO",
                "payload": {
                    "uno_player": uno_player,
                    "player": player 
                }
            }))
        self.game.uno_player = uno_player.uno = player