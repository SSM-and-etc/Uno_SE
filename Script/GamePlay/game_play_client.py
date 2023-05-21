import pygame

from uno.game import Game
from uno.player import Player
from uno.enums import CardColor, CardType
from Player.PlayerAI import PlayerAI
from System.option import Option

import socket

import random

import pickle

import os

class Asset:
    design_size = (1280, 720)
    user_data = None

    def __init__(self, img, pos, mag=1.0):
        self.mag = mag
        self.pos = pos
        self.img_path = None

        if isinstance(img, str):
            self.img_path = img
            if self.user_data.color_blindness_mode:
                if os.path.exists(os.path.join("Material/ColorMode", img)):
                    img = os.path.join("Material/ColorMode", img)
                else:
                    img = os.path.join("Material", img)
            else:
                img = os.path.join("Material", img)

            self.orig_img = pygame.image.load(img)
        else:
            self.orig_img = img.copy()
        self.img = pygame.transform.scale_by(self.orig_img, (self.mag, self.mag))

        self.rect = self.img.get_rect().move(pos)

    def image_reload(self):
        if self.img_path:
            self.set_image(self.img_path)

    def set_image(self, img_path):
        if self.user_data.color_blindness_mode:
            if os.path.exists(os.path.join("Material/ColorMode", img_path)):
                img_path = os.path.join("Material/ColorMode", img_path)
            else:
                img_path = os.path.join("Material", img_path)
        else:
            img_path = os.path.join("Material", img_path)
        

        self.orig_img = pygame.image.load(img_path)
        self.img = pygame.transform.scale_by(self.orig_img, (self.mag, self.mag))

        self.rect = self.img.get_rect().move(self.pos)

    def scaled_img(self):
        screen_size = self.user_data.get_screen_size()
        x_ratio, y_ratio = screen_size[0] / self.design_size[0], screen_size[1] / self.design_size[1]
        return pygame.transform.scale_by(self.orig_img, (self.mag * x_ratio, self.mag * y_ratio))

    def scaled_rect(self):
        screen_size = self.user_data.get_screen_size()
        x_ratio, y_ratio = screen_size[0] / self.design_size[0], screen_size[1] / self.design_size[1]

        x, y, w, h = self.rect
        x *= x_ratio
        w *= x_ratio
        y *= y_ratio
        h *= y_ratio
        return pygame.Rect(x, y, w, h) 

    def scaled(self):
        return self.scaled_img(), self.scaled_rect()

    def clone(self):
        asset = Asset(self.orig_img, self.pos, self.mag)
        asset.rect = self.rect.copy()
        return asset

    def copy(self, asset):
        self.mag = asset.mag
        self.pos = asset.pos
        self.img = asset.img.copy()
        self.rect = asset.rect

class FakeAsset(Asset):
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)

class Selection:
    def __init__(self, player, color_selection):
        self.map = [
            ["deck", "button_uno"],
            list(CardColor),
            ["card"]
        ]
        self.pos = [2, 0] # card[0]
        self.player = player
        self.color_selection = color_selection

    def reset(self):
        self.pos = [2, 0]

    def current(self):
        if self.pos[0] == 2:
            return "card", self.pos[1]

        else:
            return self.map[self.pos[0]][self.pos[1]], 0

    def set(self, obj, idx=0):
        if obj == "card":
            self.pos = [2, idx]

        else:
            for i, row in enumerate(self.map):
                for j, col in enumerate(row):
                    if col == obj:
                        self.pos = [i, j]
                        return

    def left(self):
        if self.pos[1] > 0:
            self.pos[1] -= 1

    def right(self):
        if self.pos[0] == 2:
            if self.pos[1] < len(self.player.hand)-1:
                self.pos[1] += 1
        else:
            if self.pos[1] < len(self.map[self.pos[0]])-1:
                self.pos[1] += 1

    def down(self):
        if self.pos[0] < 2:
            self.pos[0] += 1
            self.pos[1] = 0

        if self.pos[0] == 1 and not self.color_selection["selecting"]:
            self.pos[0] = 2

    def up(self):
        if self.pos[0] > 0:
            self.pos[0] -= 1
            self.pos[1] = 0

        if self.pos[0] == 1 and not self.color_selection["selecting"]:
            self.pos[0] = 0

class GamePlayClient:
    def __init__(self, main, stage_index = 1, server = None):
        self.main = main
        self.stage_index = stage_index
        self.user_data = main.user_data
        Asset.user_data = main.user_data
        self.option = Option(main, self)
        self.on_option = False
        self.on_game_gui = False
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

        self.winner = None
        self.result_asset = Asset("BG/result.png", (0, 0))

        self.card_assets = []
        self.hand_assets = []
        self.animate_assets = []

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.connect(("127.0.0.1", 12345))

        self.server = server
        self.server.setblocking(0)

        self.font_resize() 

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

        except:
            pass
        
    def update_table(self, only_asset=False):
        card = self.game.table.top()
        if card.is_color():
            filename = card.color + "_" + card.card_type.split("_")[1]
        else:
            filename = "wild_" + card.card_type.split("_")[1]
        self.assets["table"].set_image(f"Card/{filename}.png")

        color = self.game.table.get_color()
        self.assets["color"].set_image(f"Extra/{color}.png")

        self.hand_assets = []
        for i, player in enumerate(self.game.players):
            if player == self.player:
                self.hand_assets.append(None)
            else:
                w, y, mag = self.calculate_card_size(i)
                assets = []
                for j in range(len(player.hand)):
                    assets.append(Asset(self.assets["deck"].orig_img, (10 + self.pane_assets[i].rect[0] + w*j, 30 + y), mag))
                self.hand_assets.append(assets)

        if not only_asset:
            # uno버튼에 의한 드로우 처리
            if len(self.game.turn().hand) == 1 and self.game.turn().uno != self.game.turn():
                self.game.turn().uno = None
                if self.game.deck.stack:
                    self.animate_assets.append((self.assets["deck"].clone(), self.pane_assets[self.game.players.index(self.game.turn())], 50, 0))
                    self.game.draw(self.game.turn(), 1)  
                else:
                    self.game.draw(self.game.turn(), 1) 
            
            pygame.time.set_timer(pygame.USEREVENT, 1000)
            self.counter = 15

            for player in self.game.players:
                if len(player.hand) == 0:
                    self.winner = player

    def calculate_card_size(self, player_num):
        n = max(1, len(self.game.players[player_num].hand))

        pane_asset = self.pane_assets[player_num]
        pane_x, pane_y, pane_w, pane_h = pane_asset.rect

        card_orig = 388, 562

        card_x = (pane_w - 20) / n
        mag = card_x / card_orig[0]
        card_h = card_orig[1] * mag

        if card_h > (pane_h - 20) * 0.8:
            card_h = (pane_h - 20) * 0.8
            mag = card_h / card_orig[1]
            card_x = card_orig[0] * mag

        return card_x, pane_y + (pane_h-card_h) / 2, mag * 0.9

    def update_hand(self, only_asset=False):
        card_size = self.calculate_card_size(self.players.index(self.player))

        self.card_assets = []
        for i, card in enumerate(self.player.hand):
            if card.is_color():
                filename = card.color + "_" + card.card_type.split("_")[1]
            else:
                filename = "wild_" + card.card_type.split("_")[1]
            self.card_assets.append(Asset(f"Card/{filename}.png", (10+card_size[0]*i, 30+card_size[1]), mag=card_size[2]))
            
        if not only_asset:
            if self.color_selection["selecting"]:
                self.color_selection["selecting"] = False

            self.selection.reset()
    
    def option_closed(self):
        for name, asset in self.assets.items():
            asset.image_reload()
        for color, asset in self.color_selection["assets"].items():
            asset.image_reload()

        self.update_table(only_asset=True)
        self.update_hand(only_asset=True)

        self.font_resize()

    def font_resize(self):
        screen_size = self.user_data.get_screen_size()
        design_size = (1280, 720)
        ratio = screen_size[0] / design_size[0]
        self.counter_font = pygame.font.SysFont(None, int(50 * ratio))
        self.result_font = pygame.font.SysFont(None, int(100 * ratio))
        self.name_font = pygame.font.SysFont(None, int(40 * ratio))

    def display(self, main):
        self.socket_handle()

        if self.game:
            if self.on_option:
                self.on_option = self.option.display(main)

                if not self.on_option:
                    self.option_closed()

            elif self.winner:
                self.draw_result()

                for event in pygame.event.get():
                    if event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.KEYDOWN:
                        if self.stage_index != 0:
                            self.user_data.story_level = self.stage_index
                            self.user_data.save_data()
                        main.scene_change(main.get_scene_index("title"))

            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.main.running = False
                        
                    if event.type == pygame.KEYDOWN:
                        self.keydown_game(main, event.key)
                    
                    if event.type == pygame.MOUSEBUTTONDOWN: 
                        if not self.game.table.top().is_special():
                            if self.collide_game(event.pos):
                                self.handle()
                        
                    if event.type == pygame.MOUSEMOTION:
                        if not self.game.table.top().is_special():
                            self.collide_game(event.pos)
                    
                    if event.type == pygame.USEREVENT:
                        self.counter_event()
                            
                self.main.screen.blit(*self.assets["background"].scaled())

                if self.on_game_gui:
                    self.draw_game()
    
    def counter_event(self):
        if self.counter > 0:
            self.counter -= 1

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
                    
    def animate_asset(self):
        if self.animate_assets:
            pygame.time.set_timer(pygame.USEREVENT, 0)
            asset, dest, time, tick = self.animate_assets.pop()

            if tick >= time:
                new_rect = dest.rect
                self.update_table()
                self.update_hand()

            else:
                new_rect = asset.pos[0] - ((asset.pos[0] - dest.rect[0]) * tick / time),\
                        asset.pos[1] - ((asset.pos[1] - dest.rect[1]) * tick / time),\
                        abs(asset.rect[2] - (asset.rect[2] - dest.rect[2]) / (time-tick)*5),\
                        abs(asset.rect[3] - (asset.rect[3] - dest.rect[3]) / (time-tick)*5),\
                        
                asset.rect.update(new_rect)
                
                self.animate_assets.append((asset, dest, time, tick+1))

    def move_cursor(self):
        sel, idx = self.selection.current()
        asset = None
        if sel == "card":
            asset = self.card_assets[idx]
        elif isinstance(sel, CardColor):
            asset = self.color_selection["assets"][sel]
        else:
            asset = self.assets[sel]

        pos_x = asset.rect.centerx - 10
        pos_y = asset.rect.top - 40
        self.assets["cursor"].rect.update(pos_x, pos_y, 0, 0)
            
    def draw_game(self):
        self.animate_asset()
        try:
            self.move_cursor()
        except:
            pass

        if self.game.turn().uno:
            self.assets["button_uno"].set_image("Button/button_uno_enabled.png")
        else:
            self.assets["button_uno"].set_image("Button/button_uno.png")
        
        for name, asset in self.assets.items():
            self.main.screen.blit(*asset.scaled())

        for card_asset in self.card_assets:
            self.main.screen.blit(*card_asset.scaled())

        for i, pane_asset in enumerate(self.pane_assets):
            if self.player != self.players[i]:
                self.main.screen.blit(*pane_asset.scaled())

                for hand_asset in self.hand_assets[i]:
                    self.main.screen.blit(*hand_asset.scaled())

            self.main.screen.blit(self.name_font.render(self.game.players[i].tag, True, (255, 255, 255)), pane_asset.scaled_rect().move(5, 5))

            if self.game.players[i] == self.game.turn():
                pygame.draw.rect(self.main.screen, (255, 0, 0), pane_asset.scaled_rect(), 2)

        for asset in self.animate_assets:
            self.main.screen.blit(*asset[0].scaled())

        if self.color_selection["selecting"]:
            for color, asset in self.color_selection["assets"].items():
                self.main.screen.blit(*asset.scaled())

        self.main.screen.blit(*self.assets["table"].scaled())
        self.main.screen.blit(self.counter_font.render(str(self.counter), True, (255, 255, 255)), self.fake_assets["counter"].scaled_rect())

    def draw_result(self):
        font = self.result_font.render(self.winner.tag, True, (0, 0, 0))
        self.main.screen.blit(*self.result_asset.scaled())
        self.main.screen.blit(font, font.get_rect(center=(640, 360)))

    def collide_game(self, mouse_pos):
        if self.assets["button_uno"].scaled_rect().collidepoint(mouse_pos):
            self.selection.set("button_uno")
            return True

        if self.assets["deck"].scaled_rect().collidepoint(mouse_pos):
            self.selection.set("deck")
            return True

        for i, card_asset in enumerate(self.card_assets):
            if card_asset.scaled_rect().collidepoint(mouse_pos):
                self.selection.set("card", i)
                return True

        if self.color_selection["selecting"]:
            for color, asset in self.color_selection["assets"].items():
                if asset.scaled_rect().collidepoint(mouse_pos):
                    self.selection.set(color)
                    return True

        return False
        
    def handle(self):
        sel, idx = self.selection.current()

        if sel == "card":
            if self.game.turn() == self.player:
                if idx < len(self.player.hand) and self.game.table.playable(self.player.hand[idx]):
                    if self.player.hand[idx].card_type == CardType.CARD_CHANGECOLOR:
                        self.color_selection["selecting"] = True
                        self.color_selection["idx"] = idx

                    else:
                        self.animate_assets.append((self.card_assets[idx], self.assets["table"], 50, 0))
                        self.play_player(self.player, self.player.hand[idx])    

        elif sel == "deck":
            if self.game.turn() == self.player:
                if self.game.deck.stack:
                    self.animate_assets.append((self.assets["deck"].clone(), self.card_assets[-1], 50, 0))
                    self.play_player(self.player)
                else:
                    self.play_player(self.player)
                    self.update_table()

        elif sel == "button_uno":
            if self.possible_push_uno(self.game.turn()):
                self.play_uno(self.game.turn(), self.player)
                print("uno!")
                # TODO: SEND UNO to SERVER

        elif isinstance(sel, CardColor):
            self.player.hand[self.color_selection["idx"]].color = sel

            self.animate_assets.append((self.card_assets[self.color_selection["idx"]], self.assets["table"], 50, 0))
            self.play_player(self.player, self.player.hand[self.color_selection["idx"]])

            self.color_selection["selecting"] = False
    
    def keydown_game(self, main, key):
        if key == self.user_data.key_left:
            self.selection.left()
        elif key == self.user_data.key_right:
            self.selection.right()
        elif key == self.user_data.key_up:
            self.selection.up()
        elif key == self.user_data.key_down:
            self.selection.down()
        elif key == self.user_data.key_enter:
            self.handle()
        elif key == pygame.K_ESCAPE:
            self.on_option = True
            
    def possible_push_uno(self, now_player):
        if not now_player.uno and len(now_player.hand) <= 2: # TODO: 디버깅용으로 >=2로 설정함, <=2로 바꿔야함
            return True
        else:
            return False
        

    def apply_state_change(self):
        # TODO: 현재 state에 따라 select 이미지 적절하게 이동시키기
        pass
    
    def enter_state(self, main):
        pass


    '''
        if(self.select_state == STATE_SINGLE_GAME):
            # TODO: 싱글 게임 시작 호출 
            pass
        elif(self.select_state == STATE_OPTION):
            self.on_title_gui = False
            # TODO: 옵션창 호출
            pass
        elif(self.select_state == STATE_EXIT):
            main.running = False
    '''
    
    def change_screen_size(self):
        pass # title의 size 변경 방식과의 호환을 위해 임시로 만듦